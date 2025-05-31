import cv2
import numpy as np
import mediapipe as mp
import json
from utils.logging_config import logger
import traceback

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils

# Create a context manager for the pose processor
class PoseProcessor:
    def __init__(self, static_image_mode=True, min_detection_confidence=0.3, model_complexity=2):
        self.static_image_mode = static_image_mode
        self.min_detection_confidence = min_detection_confidence
        self.model_complexity = model_complexity
        self.pose = None
                                  
    def __enter__(self):
        self.pose = mp_pose.Pose(
            static_image_mode=self.static_image_mode,
            min_detection_confidence=self.min_detection_confidence,
            model_complexity=self.model_complexity
        )
        return self.pose
        
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.pose:
            self.pose.close()

def preprocess_image(image):
    """Preprocess the image to enhance pose detection."""
    try:
        # Convert to RGB for MediaPipe
        rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Resize if too large (MediaPipe works better with smaller images)
        height, width = rgb_image.shape[:2]
        max_dimension = 640
        if width > max_dimension or height > max_dimension:
            scale = max_dimension / max(width, height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            rgb_image = cv2.resize(rgb_image, (new_width, new_height))
        
        # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
        # Split into channels
        r, g, b = cv2.split(rgb_image)
        
        # Create CLAHE object
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        
        # Apply CLAHE to each channel
        r_clahe = clahe.apply(r)
        g_clahe = clahe.apply(g)
        b_clahe = clahe.apply(b)
        
        # Merge channels back
        rgb_image = cv2.merge([r_clahe, g_clahe, b_clahe])
        
        # Apply slight Gaussian blur to reduce noise
        rgb_image = cv2.GaussianBlur(rgb_image, (3, 3), 0)
        
        # Convert back to BGR for OpenCV operations
        return cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
    except Exception as e:
        logger.error(f"Error in preprocessing image: {str(e)}")
        logger.debug(traceback.format_exc())
        return image

def process_image(image):
    """Processes an image for pose detection and returns the output image."""
    try:
        # Validate input
        if image is None:
            logger.error("Invalid image input: image is None")
            return None
            
        # Check image dimensions
        height, width = image.shape[:2]
        if width < 64 or height < 64:  # Minimum reasonable size
            logger.error(f"Image too small: {width}x{height}")
            return None
            
        # Check image format
        if len(image.shape) != 3 or image.shape[2] != 3:
            logger.error(f"Invalid image format: expected 3 channels, got {len(image.shape) if len(image.shape) > 2 else 1}")
            return None

        # Preprocess the image
        processed_img = preprocess_image(image)
        
        # Convert to RGB for MediaPipe
        imgRGB = cv2.cvtColor(processed_img, cv2.COLOR_BGR2RGB)
        
        # Process image with proper resource management
        with PoseProcessor(
            static_image_mode=False,  # Changed to False for better detection
            min_detection_confidence=0.3,
            model_complexity=2
        ) as pose:
            result = pose.process(imgRGB)

            # Create output image
            output_img = image.copy()
            
            # Draw landmarks if detected
            if result.pose_landmarks:
                # Draw connections with thicker lines
                mp_drawing.draw_landmarks(
                    output_img, 
                    result.pose_landmarks, 
                    mp_pose.POSE_CONNECTIONS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(
                        color=(0, 255, 0),  # green dots
                        thickness=3,
                        circle_radius=5
                    ),
                    connection_drawing_spec=mp_drawing.DrawingSpec(
                        color=(255, 255, 255),  # white lines
                        thickness=3
                    ),
                )
                
                # Log detection success
                logger.info(f"Pose detected in image: {width}x{height}")
                return output_img
            else:
                logger.warning(f"No pose detected in image: {width}x{height}")
                return None
            
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        logger.debug(traceback.format_exc())
        return None
