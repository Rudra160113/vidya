# File location: vidya/data/database_connector.py

import logging
import sqlite3

class DatabaseConnector:
    """
    A generic connector for different types of databases.
    This example uses SQLite for simplicity.
    """
    def __init__(self, db_path: str = 'vidya_data.db'):
        self.db_path = db_path
        self.conn = None
        logging.info("DatabaseConnector initialized.")
        self.connect()

    def connect(self):
        """Establishes a connection to the database."""
        try:
            self.conn = sqlite3.connect(self.db_path)
            logging.info(f"Connected to database at '{self.db_path}'.")
        except sqlite3.Error as e:
            logging.error(f"Failed to connect to the database: {e}")
            raise ConnectionError(f"Could not connect to the database: {e}")

    def close(self):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            logging.info("Database connection closed.")
            
    def execute_query(self, query: str, params: tuple = ()) -> list:
        """
        Executes a query and returns the results.
        Note: This is a simplified version and does not handle all query types.
        """
        if not self.conn:
            raise ConnectionError("No database connection. Please call .connect() first.")
        
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, params)
            self.conn.commit()
            logging.debug(f"Query executed successfully: {query}")
            return cursor.fetchall()
        except sqlite3.Error as e:
            logging.error(f"Error executing query '{query}': {e}")
            return []

    def setup_database(self):
        """Creates the necessary tables for the application."""
        create_history_table = """
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            source TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        create_knowledge_base_table = """
        CREATE TABLE IF NOT EXISTS knowledge_base (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source_url TEXT NOT NULL,
            content TEXT NOT NULL,
            ingested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.execute_query(create_history_table)
        self.execute_query(create_knowledge_base_table)
        logging.info("Database tables verified/created.")
