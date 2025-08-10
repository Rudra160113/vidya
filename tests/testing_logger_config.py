# File location: vidya/tests/testing_logger_config.py

import logging
import unittest.mock
import io
import contextlib
from vidya.tests.testing_framework import TestingFramework
from vidya.utils.logger_config import setup_logging

class TestingLoggerConfig:
    """
    A suite of tests to verify the functionality of the logging configuration.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        logging.info("TestingLoggerConfig initialized.")
    
    def test_logging_setup(self) -> bool:
        """Tests if logging is configured to capture messages correctly."""
        # Use a string stream to capture log output
        log_stream = io.StringIO()
        
        # Temporarily configure logging to write to our stream
        with contextlib.redirect_stderr(log_stream):
            setup_logging(log_level='DEBUG', log_file='testing.log')
            
            logger = logging.getLogger('vidya')
            logger.debug("Debug message.")
            logger.info("Info message.")
            logger.warning("Warning message.")
            
        log_output = log_stream.getvalue()
        
        # Check if the messages are in the output and formatted correctly
        debug_message_present = "DEBUG - Debug message." in log_output
        info_message_present = "INFO - Info message." in log_output
        warning_message_present = "WARNING - Warning message." in log_output
        
        # The logging file 'testing.log' is also created, but we don't test its content directly here.
        return debug_message_present and info_message_present and warning_message_present

    def run_all_tests(self):
        """Runs all logging configuration tests."""
        self.test_runner.run_test("Logging Setup Test", self.test_logging_setup)
        self.test_runner.print_summary()
