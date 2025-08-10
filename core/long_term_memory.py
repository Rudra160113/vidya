# File location: vidya/core/long_term_memory.py

import logging
from vidya.data.database_connector import DatabaseConnector

class LongTermMemory:
    """
    Manages the long-term memory of the AI by storing and retrieving
    information from the database.
    """
    def __init__(self, db_connector: DatabaseConnector):
        self.db_connector = db_connector
        logging.info("LongTermMemory initialized.")
        self._setup_table()
        
    def _setup_table(self):
        """Creates the long_term_memory table if it doesn't exist."""
        create_table = """
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            category TEXT NOT NULL,
            key TEXT NOT NULL,
            value TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.db_connector.execute_query(create_table)
        logging.info("Long-term memory table verified/created.")

    def store_information(self, user_id: str, category: str, key: str, value: str) -> str:
        """
        Stores a piece of information in the long-term memory.
        """
        try:
            insert_query = "INSERT INTO long_term_memory (user_id, category, key, value) VALUES (?, ?, ?, ?)"
            self.db_connector.execute_query(insert_query, (user_id, category, key, value))
            logging.info(f"Information stored for '{user_id}': {key} -> {value}")
            return "Information successfully stored in long-term memory."
        except Exception as e:
            logging.error(f"Failed to store information: {e}")
            return "An error occurred while storing the information."
            
    def retrieve_information(self, user_id: str, key: str) -> str:
        """
        Retrieves a piece of information from the long-term memory.
        """
        query = "SELECT value FROM long_term_memory WHERE user_id=? AND key=? ORDER BY timestamp DESC LIMIT 1"
        result = self.db_connector.execute_query(query, (user_id, key))
        
        if result:
            logging.info(f"Retrieved information for '{user_id}': {key} -> {result[0][0]}")
            return result[0][0]
        else:
            logging.warning(f"No information found for '{user_id}' with key '{key}'.")
            return ""
