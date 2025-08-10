# File location: vidya/core/error_handler.py

import logging
import traceback

class ErrorHandler:
    """
    Centralized handler for logging and managing application errors.
    """
    def __init__(self, logger: logging.Logger = logging.getLogger(__name__)):
        self.logger = logger
        self.error_count = 0
        self.last_error = None
        self.last_error_traceback = None
        self.logger.info("ErrorHandler initialized.")

    def handle_exception(self, exception: Exception, context: str):
        """
        Logs a detailed exception with its traceback and context.
        """
        self.error_count += 1
        self.last_error = str(exception)
        self.last_error_traceback = traceback.format_exc()
        
        self.logger.error(f"An exception occurred in '{context}': {exception}")
        self.logger.error("Traceback:\n" + self.last_error_traceback)

    def get_error_report(self) -> dict:
        """
        Returns a summary of the most recent error.
        """
        return {
            "error_count": self.error_count,
            "last_error": self.last_error,
            "last_error_traceback": self.last_error_traceback
        }

    def clear_errors(self):
        """
        Resets the error count and history.
        """
        self.error_count = 0
        self.last_error = None
        self.last_error_traceback = None
        self.logger.info("Error history cleared.")
