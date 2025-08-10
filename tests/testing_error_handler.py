# File location: vidya/tests/testing_error_handler.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.core.error_handler import ErrorHandler

class TestingErrorHandler:
    """
    A suite of tests to verify the functionality of the ErrorHandler.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.handler = ErrorHandler()
        logging.info("TestingErrorHandler initialized.")
    
    def _mock_function_that_fails(self):
        """A function that simulates a runtime error."""
        raise ValueError("Simulated error message.")

    def _mock_function_that_succeeds(self):
        """A function that runs without errors."""
        return "Success!"

    def test_handle_exception(self) -> bool:
        """Tests if the handler correctly catches and processes an exception."""
        with unittest.mock.patch.object(logging.getLogger('vidya'), 'error') as mock_log:
            result = self.handler.handle_exception(self._mock_function_that_fails, "Test failure")
            
            # The handler should log the error
            mock_log.assert_called_once()
            
            # The result should be the formatted error message
            return "Test failure" in result and "ValueError" in result
            
    def test_no_exception(self) -> bool:
        """Tests if the handler works correctly when no exception is raised."""
        with unittest.mock.patch.object(logging.getLogger('vidya'), 'error') as mock_log:
            result = self.handler.handle_exception(self._mock_function_that_succeeds, "Test success")
            
            # The handler should not log an error
            mock_log.assert_not_called()
            
            # The result should be the successful return value
            return result == "Success!"

    def run_all_tests(self):
        """Runs all error handler tests."""
        self.test_runner.run_test("Handle Exception Test", self.test_handle_exception)
        self.test_runner.run_test("No Exception Test", self.test_no_exception)
        self.test_runner.print_summary()
