# File location: vidya/tests/testing_custom_logger.py

import logging
import os
import io
import sys
from vidya.tests.testing_framework import TestingFramework
from vidya.utils.custom_logger import setup_logger

class TestingCustomLogger:
    """
    A suite of tests to verify the functionality of the CustomLogger.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.log_file = "test.log"
        logging.info("TestingCustomLogger initialized.")

    def _cleanup(self):
        """Removes the temporary log file."""
        if os.path.exists(self.log_file):
            os.remove(self.log_file)

    def test_console_logging(self) -> bool:
        """Tests if the logger logs to the console correctly."""
        self._cleanup()
        
        # Capture stdout to verify logs
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        logger = setup_logger(log_level='INFO')
        logger.info("Test console message.")
        
        sys.stdout = sys.__stdout__ # Reset stdout
        
        # Check if the captured output contains the message
        return "Test console message." in captured_output.getvalue()

    def test_file_logging(self) -> bool:
        """Tests if the logger logs to a file correctly."""
        self._cleanup()
        
        logger = setup_logger(log_level='INFO', log_file=self.log_file)
        logger.info("Test file message.")
        
        # The logger might need a moment to write to the file
        logging.shutdown()
        
        if not os.path.exists(self.log_file):
            return False
        
        with open(self.log_file, 'r') as f:
            content = f.read()
            
        self._cleanup()
        return "Test file message." in content

    def test_log_level_filter(self) -> bool:
        """Tests if the logger filters messages based on log level."""
        self._cleanup()
        
        captured_output = io.StringIO()
        sys.stdout = captured_output
        
        logger = setup_logger(log_level='INFO')
        logger.debug("This should not be logged.")
        logger.info("This should be logged.")
        
        sys.stdout = sys.__stdout__
        
        return "This should be logged." in captured_output.getvalue() and "This should not be logged." not in captured_output.getvalue()

    def run_all_tests(self):
        """Runs all custom logger tests."""
        self.test_runner.run_test("Console Logging Test", self.test_console_logging)
        self.test_runner.run_test("File Logging Test", self.test_file_logging)
        self.test_runner.run_test("Log Level Filter Test", self.test_log_level_filter)
        self.test_runner.print_summary()
