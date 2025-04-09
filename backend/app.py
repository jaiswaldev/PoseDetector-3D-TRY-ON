from flask import Flask, request, jsonify, Response
from flask_socketio import SocketIO, emit
import base64
import cv2
import numpy as np
from flask_cors import CORS
from utils.logging_config import logger
from controllers.image_controller import process_image
from controllers.video_controller import generate_frames, release_camera

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# const cors = require("cors");
CORS(app, resources={r"/api/*": {"origins": "*"}})
# app.use(cors({ origin: "http://localhost:5173", methods: ["GET", "POST"] }));


@app.route('/')
def home():
    return "Hello, World!"
    
@app.route('/api/v1/image', methods=['POST'])
def detect_pose_from_image():
    """Endpoint to detect pose from an uploaded image."""
    data = request.get_json()
    if not data or 'image' not in data:
        return jsonify({"error": "Invalid request"}), 400

    try:
        image_data = base64.b64decode(data['image'])
        np_image = np.frombuffer(image_data, np.uint8)
        image = cv2.imdecode(np_image, cv2.IMREAD_COLOR)

        output_img = process_image(image)

        _, buffer = cv2.imencode('.jpg', output_img)
        base64_output = base64.b64encode(buffer).decode('utf-8')

        return jsonify({"image": base64_output})
    except Exception as e:
        logger.error(f"Error in pose detection: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/v1/live-video', methods=['GET'])
def video_feed():
    """Route to stream live video with pose detection."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@socketio.on('connect')
def handle_connect():
    logger.info('WebSocket connection established.')

@socketio.on('video_frame')
def handle_video_frame(data):
    """Receive video frames from frontend, process, and return pose landmarks."""
    try:
        frame = base64_to_image(data)
        if frame is not None:
            output_img = process_image(frame)

            _, buffer = cv2.imencode('.jpg', output_img)
            base64_output = base64.b64encode(buffer).decode('utf-8')

            emit('pose_data', {"image": base64_output})
        else:
            logger.error("Invalid frame received.")
    except Exception as e:
        logger.error(f"Error processing video frame: {e}")
        emit('error', {"error": str(e)})

def base64_to_image(base64_string):
    """Convert base64-encoded string to OpenCV image."""
    try:
        img_data = base64.b64decode(base64_string)
        np_arr = np.frombuffer(img_data, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        logger.error(f"Decoding Error: {e}")
        return None

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=8000, debug=True)
