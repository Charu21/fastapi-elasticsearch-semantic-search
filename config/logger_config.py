import os
import logging
from datetime import datetime

class LoggerConfig:
    @staticmethod
    def configure_logging():
        log_level = os.getenv('LOG_LEVEL', 'INFO').upper()
        numeric_level = getattr(logging, log_level, logging.INFO)
        current_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_filename = os.getenv('LOG_FILE', f'app_{current_time}.log')
        
        logging.basicConfig(
            level=numeric_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
                logging.StreamHandler()
            ]
        )
        logging.info(f"Logging configured at {log_level} level")
