# File location: vidya/tests/testing_conversation_service.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.core.conversation_service import ConversationService

class TestingConversationService:
    """
    A suite of tests to verify the functionality of the ConversationService.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.service = ConversationService()
        logging.info("TestingConversationService initialized.")

    def test_add_and_retrieve_message(self) -> bool:
        """Tests if messages can be added and retrieved correctly for a user."""
        user_id = "test_user_1"
        self.service.add_message(user_id, "user", "Hello, Vidya.")
        self.service.add_message(user_id, "assistant", "Hello! How can I help?")
        
        history = self.service.get_history(user_id)
        
        return len(history) == 2 and history[0]['content'] == "Hello, Vidya."

    def test_separate_user_histories(self) -> bool:
        """Tests that conversation histories for different users are kept separate."""
        user_id_1 = "test_user_1"
        user_id_2 = "test_user_2"
        
        self.service.add_message(user_id_1, "user", "History for user 1.")
        self.service.add_message(user_id_2, "user", "History for user 2.")
        
        history_1 = self.service.get_history(user_id_1)
        history_2 = self.service.get_history(user_id_2)
        
        return len(history_1) == 1 and len(history_2) == 1 and history_1[0]['content'] != history_2[0]['content']

    def test_get_context(self) -> bool:
        """Tests if the service returns the correct number of recent messages for context."""
        user_id = "test_user_3"
        for i in range(10):
            self.service.add_message(user_id, "user", f"Message {i+1}")
            
        context = self.service.get_context(user_id, n_messages=3)
        
        return len(context) == 3 and context[0]['content'] == "Message 8"

    def test_clear_history(self) -> bool:
        """Tests if the conversation history can be cleared."""
        user_id = "test_user_4"
        self.service.add_message(user_id, "user", "Message to be cleared.")
        self.service.clear_history(user_id)
        
        history = self.service.get_history(user_id)
        
        return len(history) == 0

    def run_all_tests(self):
        """Runs all conversation service tests."""
        self.test_runner.run_test("Add and Retrieve Message Test", self.test_add_and_retrieve_message)
        self.test_runner.run_test("Separate User Histories Test", self.test_separate_user_histories)
        self.test_runner.run_test("Get Context Test", self.test_get_context)
        self.test_runner.run_test("Clear History Test", self.test_clear_history)
        self.test_runner.print_summary()
