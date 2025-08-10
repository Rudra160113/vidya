# File location: vidya/utils/custom_logger.py

import logging
import sys

def setup_logger(log_level: str = 'INFO', log_file: str | None = None):
    """
    Sets up a custom logger for the Vidya application.
    
    Args:
        log_level (str): The minimum level of logs to capture (e.g., 'DEBUG', 'INFO').
        log_file (str): Optional path to a file for logging. If None, logs to console.
    """
    logger = logging.getLogger("vidya")
    
    # Set the root logger's level
    logger.setLevel(log_level)
    
    # Create a formatter for the log messages
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Remove any existing handlers to prevent duplicate logs
    if logger.hasHandlers():
        logger.handlers.clear()
        
    # If a log file is specified, create a file handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        
    # Always create a console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    logging.info("Custom logger set up.")
    return logger
