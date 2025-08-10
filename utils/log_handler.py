# File location: vidya/utils/log_handler.py

import logging
import os
import datetime

class LogHandler:
    """
    Configures and manages logging for the entire application.
    """
    def __init__(self, log_level: str = 'INFO', log_file: str = 'vidya.log'):
        self.log_level = log_level.upper()
        self.log_file = log_file
        self.log_dir = 'logs'
        
        if not os.path.exists(self.log_dir):
            os.makedirs(self.log_dir)

        self._setup_logging()
        logging.info("LogHandler initialized.")

    def _setup_logging(self):
        """
        Configures the logging format and handlers.
        """
        log_path = os.path.join(self.log_dir, self.log_file)
        
        # Define the logging format
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # File Handler
        file_handler = logging.FileHandler(log_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.getLevelName(self.log_level))

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        console_handler.setLevel(logging.getLevelName(self.log_level))

        # Root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.getLevelName(self.log_level))
        root_logger.addHandler(file_handler)
        root_logger.addHandler(console_handler)

    def get_logger(self, name: str) -> logging.Logger:
        """
        Returns a named logger for a specific module.
        """
        return logging.getLogger(name)

    def log_message(self, level: str, message: str, name: str = __name__):
        """
        Logs a message with a specific level.
        """
        logger = self.get_logger(name)
        if level.upper() == 'INFO':
            logger.info(message)
        elif level.upper() == 'WARNING':
            logger.warning(message)
        elif level.upper() == 'ERROR':
            logger.error(message)
        elif level.upper() == 'DEBUG':
            logger.debug(message)
