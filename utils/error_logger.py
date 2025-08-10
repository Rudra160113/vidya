# File location: vidya/utils/error_logger.py

import logging
import datetime
import traceback
import os

class ErrorLogger:
    """
    A utility to log errors and exceptions in a structured way.
    """
    def __init__(self, log_directory: str = 'logs'):
        self.log_directory = log_directory
        if not os.path.exists(self.log_directory):
            os.makedirs(self.log_directory)
        self.log_filename = os.path.join(self.log_directory, 'errors.log')
        
        logging.basicConfig(
            filename=self.log_filename,
            level=logging.ERROR,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        logging.info("ErrorLogger initialized.")

    def log_error(self, message: str, exception: Exception = None):
        """
        Logs an error message and, optionally, a full traceback.
        """
        full_message = f"Error: {message}"
        if exception:
            full_message += f"\nException Type: {type(exception).__name__}\nTraceback:\n{traceback.format_exc()}"
        
        logging.error(full_message)
        
        # Also print to console for immediate visibility
        print(f"ERROR: {message}")
        if exception:
            print(f"Exception Type: {type(exception).__name__}")

    def get_latest_errors(self, num_lines: int = 20) -> str:
        """
        Retrieves the last N lines from the error log file.
        """
        try:
            with open(self.log_filename, 'r') as f:
                lines = f.readlines()
                return "".join(lines[-num_lines:])
        except FileNotFoundError:
            return "Error log file not found."
        except Exception as e:
            return f"An error occurred while reading the error log: {e}"
