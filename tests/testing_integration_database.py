# File location: vidya/tests/testing_integration_database.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.data.database_connector import DatabaseConnector
from vidya.user.user_profile_manager import UserProfileManager
from vidya.core.long_term_memory import LongTermMemory
from vidya.data.chat_history import ChatHistory

class TestingIntegrationDatabase:
    """
    A suite of integration tests focused on database interactions.
    """
    def __init__(self):
        # Use a fresh, in-memory database for each test run to ensure isolation
        self.db_connector = DatabaseConnector(db_path=':memory:')
        self.db_connector.setup_database()
        
        # Instantiate components that interact with the database
        self.user_profile_manager = UserProfileManager(self.db_connector)
        self.long_term_memory = LongTermMemory(self.db_connector)
        self.chat_history = ChatHistory(self.db_connector)
        
        self.test_runner = TestingFramework()
        logging.info("TestingIntegrationDatabase initialized with in-memory DB.")

    def test_user_profile_creation(self) -> bool:
        """Tests if a user profile can be created and retrieved."""
        user_id = "test_user_db_1"
        self.user_profile_manager.create_user_profile(user_id, "Test Name")
        profile = self.user_profile_manager.get_user_profile(user_id)
        
        return profile is not None and profile.get('name') == "Test Name"

    def test_long_term_memory_storage(self) -> bool:
        """Tests if information can be stored and retrieved from long-term memory."""
        user_id = "test_user_db_2"
        key = "favorite_color"
        value = "blue"
        self.long_term_memory.store_information(user_id, "preference", key, value)
        retrieved_value = self.long_term_memory.retrieve_information(user_id, key)
        
        return retrieved_value == value

    def test_chat_history_logging(self) -> bool:
        """Tests if chat history messages are logged correctly."""
        user_id = "test_user_db_3"
        message = "Hello Vidya"
        self.chat_history.log_message(user_id, "user", message)
        history = self.chat_history.get_history(user_id)
        
        return len(history) == 1 and history[0].get('message') == message

    def run_all_tests(self):
        """Runs all database-related integration tests."""
        self.test_runner.run_test("User Profile DB Test", self.test_user_profile_creation)
        self.test_runner.run_test("Long-Term Memory DB Test", self.test_long_term_memory_storage)
        self.test_runner.run_test("Chat History DB Test", self.test_chat_history_logging)
        self.test_runner.print_summary()
        self.db_connector.close()
