# File location: vidya/core/analytics_engine.py

import logging
import json
from datetime import datetime
from vidya.data.database_connector import DatabaseConnector

class AnalyticsEngine:
    """
    Collects and analyzes user interaction data to provide insights.
    """
    def __init__(self, db_connector: DatabaseConnector):
        self.db_connector = db_connector
        logging.info("AnalyticsEngine initialized.")
        self._setup_table()

    def _setup_table(self):
        """Creates the analytics_events table if it doesn't exist."""
        create_table = """
        CREATE TABLE IF NOT EXISTS analytics_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            event_type TEXT NOT NULL,
            event_data TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.db_connector.execute_query(create_table)
        logging.info("Analytics events table verified/created.")

    def log_event(self, user_id: str, event_type: str, event_data: dict = None):
        """
        Logs a specific user event to the database.
        `event_data` should be a dictionary that can be serialized to JSON.
        """
        try:
            event_data_json = json.dumps(event_data) if event_data else None
            insert_query = "INSERT INTO analytics_events (user_id, event_type, event_data) VALUES (?, ?, ?)"
            self.db_connector.execute_query(insert_query, (user_id, event_type, event_data_json))
            logging.debug(f"Event logged: user='{user_id}', type='{event_type}'")
        except Exception as e:
            logging.error(f"Failed to log analytics event: {e}")

    def get_event_count(self, event_type: str) -> int:
        """
        Returns the total count of a specific event type.
        """
        query = "SELECT COUNT(*) FROM analytics_events WHERE event_type=?"
        result = self.db_connector.execute_query(query, (event_type,))
        return result[0][0] if result else 0
