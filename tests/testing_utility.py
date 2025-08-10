# File location: vidya/tests/testing_utility.py

import os
import sqlite3
from unittest.mock import MagicMock

class TestingUtility:
    """
    Provides reusable utility functions for testing the Vidya application.
    """
    @staticmethod
    def create_mock_db_connector():
        """
        Creates a mock database connector for testing without a real database.
        """
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.execute_query.side_effect = lambda query, params=None: None # Simulates a successful query
        return mock_conn

    @staticmethod
    def create_in_memory_db():
        """
        Creates a real, in-memory SQLite database for integration tests.
        Returns the connection object.
        """
        conn = sqlite3.connect(':memory:')
        return conn

    @staticmethod
    def create_dummy_config_file(path: str, content: str):
        """
        Creates a temporary config file with specified content.
        """
        with open(path, 'w') as f:
            f.write(content)

    @staticmethod
    def cleanup_file(path: str):
        """
        Deletes a file if it exists.
        """
        if os.path.exists(path):
            os.remove(path)
