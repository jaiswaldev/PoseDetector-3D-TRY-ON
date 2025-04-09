from app import app
from waitress import serve
from utils.logging_config import configure_logging
import warnings

def run_server():
    # Configure logging before anything else
    configure_logging()
    
    # Suppress TensorFlow warnings (optional)
    warnings.filterwarnings('ignore', category=UserWarning)
    
    # Import ML models after logging is configured
    # from controllers.image_controller import process_image
    
    # # Test model initialization
    # print("\n=== Server Starting ===")
    # print("Testing ML model initialization...")
    # try:
    #     # Test with dummy data
    #     import numpy as np
    #     dummy_input = np.zeros((1, 224, 224, 3), dtype=np.float32)
    #     process_image(dummy_input)  # Should complete without errors
    #     print("✓ ML models initialized successfully")
    # except Exception as e:
    #     print(f"! Model initialization failed: {str(e)}")
    #     raise

    # Start server
    print(f"\nServer ready at http://127.0.0.1:8000")
    serve(
        app,
        host='127.0.0.1',
        port=8000,
        threads=4,
        ident='PoseDetectionAPI',
        channel_timeout=60
    )

if __name__ == '__main__':
    run_server()
     