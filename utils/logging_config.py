import logging
import os
from logging.config import dictConfig
from logging.handlers import RotatingFileHandler

def configure_logging():
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    log_file = os.path.join(log_dir, 'app.log')
    
    logging_config = {
        'version': 1,
        'formatters': {
            'default': {'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'},
            'detailed': {'format': '[%(asctime)s] %(levelname)s in %(module)s [%(pathname)s:%(lineno)d]: %(message)s'}
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'INFO'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': log_file,
                'formatter': 'detailed',
                'level': 'DEBUG',
                'maxBytes': 10485760,  # 10MB
                'backupCount': 5
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['console', 'file']
        },
        'loggers': {
            'werkzeug': {
                'level': 'INFO',
                'handlers': ['console', 'file'],
                'propagate': False
            }
        }
    }
    
    dictConfig(logging_config)
    logging.info(f"Logging configured. Log file: {log_file}")

logger = logging.getLogger(__name__)
