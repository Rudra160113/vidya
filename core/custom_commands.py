# File location: vidya/core/custom_commands.py

import logging
from vidya.data.database_connector import DatabaseConnector

class CustomCommands:
    """
    Manages user-defined custom commands, allowing the AI to learn new behaviors.
    """
    def __init__(self, db_connector: DatabaseConnector):
        self.db_connector = db_connector
        logging.info("CustomCommands initialized.")
        self._setup_table()

    def _setup_table(self):
        """Creates the custom_commands table if it doesn't exist."""
        create_table = """
        CREATE TABLE IF NOT EXISTS custom_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            trigger_phrase TEXT NOT NULL,
            action TEXT NOT NULL,
            UNIQUE(user_id, trigger_phrase)
        );
        """
        self.db_connector.execute_query(create_table)
        logging.info("Custom commands table verified/created.")

    def add_command(self, user_id: str, trigger_phrase: str, action: str) -> str:
        """
        Adds a new custom command for a specific user.
        """
        try:
            insert_query = "INSERT INTO custom_commands (user_id, trigger_phrase, action) VALUES (?, ?, ?)"
            self.db_connector.execute_query(insert_query, (user_id, trigger_phrase, action))
            logging.info(f"Custom command added for user '{user_id}': '{trigger_phrase}' -> '{action}'")
            return f"Custom command '{trigger_phrase}' has been added."
        except Exception as e:
            logging.error(f"Failed to add custom command: {e}")
            return "An error occurred while adding the custom command. It may already exist."

    def get_command_action(self, user_id: str, trigger_phrase: str) -> str:
        """
        Retrieves the action associated with a custom command.
        """
        query = "SELECT action FROM custom_commands WHERE user_id=? AND trigger_phrase=?"
        result = self.db_connector.execute_query(query, (user_id, trigger_phrase))
        
        if result:
            logging.info(f"Found custom command action for '{trigger_phrase}'.")
            return result[0][0]
        else:
            return ""
