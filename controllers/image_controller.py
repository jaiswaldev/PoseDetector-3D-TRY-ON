import cv2
import numpy as np
import mediapipe as mp
import json
from utils.logging_config import logger

mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5, model_complexity=2)
mp_drawing = mp.solutions.drawing_utils

def process_image(image):
    """Processes an image for pose detection and returns the output image."""
    try:
        if image is None:
            logger.error("Invalid image input")
            return None

        imgRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        result = pose.process(imgRGB)

        output_img = image.copy()
        if result.pose_landmarks:
            mp_drawing.draw_landmarks(
                output_img, result.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                landmark_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=5, circle_radius=3),
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2),
            )

        return output_img
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return None
