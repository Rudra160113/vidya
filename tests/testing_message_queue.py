# File location: vidya/tests/testing_message_queue.py

import logging
import time
from vidya.tests.testing_framework import TestingFramework
from vidya.core.message_queue import MessageQueue

class TestingMessageQueue:
    """
    A suite of tests to verify the functionality of the MessageQueue.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.queue = MessageQueue()
        logging.info("TestingMessageQueue initialized.")
    
    def test_put_and_get_message(self) -> bool:
        """Tests if a message can be put into and retrieved from the queue."""
        message_to_send = {"type": "event", "data": "Hello, World!"}
        
        self.queue.put_message(message_to_send)
        retrieved_message = self.queue.get_message()
        
        return message_to_send == retrieved_message

    def test_queue_blocking_behavior(self) -> bool:
        """Tests if the queue blocks when retrieving from an empty queue."""
        # Use a timeout to test the blocking behavior
        start_time = time.time()
        # The get_message call should time out
        retrieved_message = self.queue.get_message(timeout=0.1)
        end_time = time.time()
        
        # Check if the message is None and if the call took approximately 0.1 seconds
        return retrieved_message is None and (end_time - start_time) >= 0.1

    def run_all_tests(self):
        """Runs all message queue tests."""
        self.test_runner.run_test("Put and Get Message Test", self.test_put_and_get_message)
        self.test_runner.run_test("Queue Blocking Test", self.test_queue_blocking_behavior)
        self.test_runner.print_summary()
