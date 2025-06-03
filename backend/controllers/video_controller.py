from state import camera, is_camera_active  # import shared state
import cv2
import mediapipe as mp
import asyncio
import time

async def generate_frames():
    import state  # to allow reassignment
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    # mp_drawing_styles = mp.solutions.drawing_styles
    pose = mp_pose.Pose(model_complexity=0)

    try:
        if state.camera is None or not state.camera.isOpened():
            state.camera = cv2.VideoCapture(0)
            if not state.camera.isOpened():
                print("Error: Could not open video stream.")
                return
            state.is_camera_active = True
            print("Camera opened.")

        while state.is_camera_active:
            success, frame = state.camera.read()
            if not success:
                break

            frame = cv2.flip(frame, 1)
            frame = cv2.resize(frame, (320, 240))
            image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

           
            results = pose.process(image_rgb)


            # print(results.pose_landmarks)

            if results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    # mp_pose.POSE_CONNECTIONS,
                    # mp_drawing_styles.get_default_pose_landmarks_style()
                )
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = frame.shape
                    print(id, lm)
                
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # cv2.putText(frame, str(id), (cx, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            cTime = time.time()
            fps = 1 / (cTime - state.prevTime)
            state.prevTime = cTime

            cv2.putText(frame, f'FPS: {int(fps)}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')

            await asyncio.sleep(0.01)

    finally:
        if state.camera and state.camera.isOpened():
            state.camera.release()
            print("Camera released.")
        state.camera = None
        state.is_camera_active = False
        pose.close()
