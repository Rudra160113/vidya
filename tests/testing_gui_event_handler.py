# File location: vidya/tests/testing_gui_event_handler.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.gui.gui_event_handler import GUIEventHandler
from vidya.core.message_queue import MessageQueue

class TestingGUIEventHandler:
    """
    A suite of tests to verify the functionality of the GUIEventHandler.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup mock dependencies
        self.mock_message_queue = unittest.mock.Mock(spec=MessageQueue)
        self.handler = GUIEventHandler(self.mock_message_queue)
        logging.info("TestingGUIEventHandler initialized.")
    
    def test_handle_button_click_event(self) -> bool:
        """Tests if a button click event is handled and a message is queued."""
        event_data = {
            "type": "click",
            "target": "submit_button",
            "payload": {"form_data": {"name": "Test User"}}
        }
        
        self.handler.handle_event(event_data)
        
        # Verify that a message was put on the queue
        self.mock_message_queue.put_message.assert_called_once()
        
        # Check the content of the message
        call_args, _ = self.mock_message_queue.put_message.call_args
        message = call_args[0]
        
        return message["event_type"] == "gui_event" and message["event_data"]["target"] == "submit_button"

    def test_handle_unknown_event_type(self) -> bool:
        """Tests if an unknown event type is handled without errors."""
        event_data = {
            "type": "unknown",
            "target": "some_element"
        }
        
        self.handler.handle_event(event_data)
        
        # The mock queue should not have been called
        self.mock_message_queue.put_message.assert_not_called()
        
        return True

    def run_all_tests(self):
        """Runs all GUI event handler tests."""
        self.test_runner.run_test("Handle Button Click Test", self.test_handle_button_click_event)
        self.test_runner.run_test("Handle Unknown Event Test", self.test_handle_unknown_event_type)
        self.test_runner.print_summary()
