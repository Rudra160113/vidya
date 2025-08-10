# File location: vidya/tests/testing_command_router.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.core.command_router import CommandRouter

class TestingCommandRouter:
    """
    A suite of tests to verify the functionality of the CommandRouter.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.router = CommandRouter()
        
        # Register some mock handlers for testing
        self.mock_handler1 = unittest.mock.Mock(return_value="Handler 1 result")
        self.mock_handler2 = unittest.mock.Mock(return_value="Handler 2 result")
        self.router.register_handler("command_one", self.mock_handler1)
        self.router.register_handler("command_two", self.mock_handler2)
        
        logging.info("TestingCommandRouter initialized.")

    def test_get_handler_success(self) -> bool:
        """Tests if a registered handler can be retrieved correctly."""
        handler = self.router.get_handler("command_one")
        
        # Verify that the correct handler was returned
        return handler is self.mock_handler1

    def test_get_handler_not_found(self) -> bool:
        """Tests if requesting an unregistered handler returns None."""
        handler = self.router.get_handler("non_existent_command")
        
        # The handler should be None
        return handler is None

    def test_handler_execution(self) -> bool:
        """Tests if a retrieved handler can be executed with its arguments."""
        handler = self.router.get_handler("command_two")
        args = {"arg1": "value"}
        result = handler(args)
        
        # Verify that the handler was called with the correct arguments
        handler.assert_called_once_with(args)
        
        return result == "Handler 2 result"

    def run_all_tests(self):
        """Runs all command router tests."""
        self.test_runner.run_test("Get Handler Success Test", self.test_get_handler_success)
        self.test_runner.run_test("Get Handler Not Found Test", self.test_get_handler_not_found)
        self.test_runner.run_test("Handler Execution Test", self.test_handler_execution)
        self.test_runner.print_summary()
