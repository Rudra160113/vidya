# File location: vidya/tests/testing_event_dispatcher.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.core.event_dispatcher import EventDispatcher

class TestingEventDispatcher:
    """
    A suite of tests to verify the functionality of the EventDispatcher.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.dispatcher = EventDispatcher()
        logging.info("TestingEventDispatcher initialized.")
    
    def test_register_and_dispatch_event(self) -> bool:
        """Tests if a handler is registered and called on event dispatch."""
        mock_handler = unittest.mock.Mock()
        
        self.dispatcher.register_handler("test_event", mock_handler)
        
        event_data = {"message": "Hello, world!"}
        self.dispatcher.dispatch_event("test_event", event_data)
        
        # Verify the handler was called with the correct data
        mock_handler.assert_called_once_with(event_data)
        
        return True

    def test_dispatch_unregistered_event(self) -> bool:
        """Tests that dispatching an unregistered event does not cause an error."""
        mock_handler = unittest.mock.Mock()
        
        self.dispatcher.register_handler("registered_event", mock_handler)
        
        # Dispatch an event with no registered handler
        self.dispatcher.dispatch_event("unregistered_event", {"data": "ignored"})
        
        # The registered handler should not have been called
        mock_handler.assert_not_called()
        
        return True

    def run_all_tests(self):
        """Runs all event dispatcher tests."""
        self.test_runner.run_test("Register and Dispatch Event Test", self.test_register_and_dispatch_event)
        self.test_runner.run_test("Dispatch Unregistered Event Test", self.test_dispatch_unregistered_event)
        self.test_runner.print_summary()
