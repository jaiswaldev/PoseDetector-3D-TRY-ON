import cv2
import numpy as np
import base64
import mediapipe as mp
from utils.logging_config import logger

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, model_complexity=2)

def generate_frames():
    """Generator function to capture live video and process pose detection."""
    camera = cv2.VideoCapture(0)  # Open webcam
    while True:
        success, frame = camera.read()
        if not success:
            break
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(rgb_frame)

        if results.pose_landmarks:
            for landmark in results.pose_landmarks.landmark:
                h, w, _ = frame.shape
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)

        _, buffer = cv2.imencode('.jpg', frame)
        frame_bytes = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

    camera.release()

def release_camera():
    """Releases camera resources."""
    cv2.VideoCapture(0).release()
    logger.info("Camera released successfully.")
