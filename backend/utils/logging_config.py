import logging
from logging.config import dictConfig

def configure_logging():
    logging_config = {
        'version': 1,
        'formatters': {
            'default': {'format': '[%(asctime)s] %(levelname)s: %(message)s'}
        },
        'handlers': {
            'console': {'class': 'logging.StreamHandler', 'formatter': 'default', 'level': 'INFO'},
            'file': {'class': 'logging.FileHandler', 'filename': 'app.log', 'formatter': 'default', 'level': 'DEBUG'}
        },
        'root': {'level': 'INFO', 'handlers': ['console', 'file']}
    }
    dictConfig(logging_config)

logger = logging.getLogger(__name__)
