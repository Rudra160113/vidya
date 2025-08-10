# File location: vidya/user/user_session_manager.py

import logging
import uuid
from datetime import datetime, timedelta
from vidya.data.session_database_connector import SessionDatabaseConnector

class UserSessionManager:
    """
    Manages user sessions, including creation, validation, and expiration.
    """
    def __init__(self, session_db_connector: SessionDatabaseConnector, session_duration_minutes: int = 60):
        self.session_db = session_db_connector
        self.session_duration = timedelta(minutes=session_duration_minutes)
        logging.info("UserSessionManager initialized.")

    def create_session(self, user_id: str) -> str:
        """
        Creates a new session for a user and returns a unique session token.
        """
        session_token = str(uuid.uuid4())
        expiry_time = datetime.now() + self.session_duration
        self.session_db.save_session(session_token, user_id, expiry_time.isoformat())
        
        logging.info(f"Session created for user '{user_id}'. Token: {session_token}")
        return session_token

    def validate_session(self, session_token: str) -> str | None:
        """
        Validates a session token and returns the user_id if valid, otherwise None.
        """
        session_data = self.session_db.get_session(session_token)
        
        if not session_data:
            logging.warning(f"Invalid session token received: {session_token}")
            return None
            
        user_id = session_data.get('user_id')
        expiry_time_str = session_data.get('expiry_time')
        
        if not expiry_time_str:
            logging.error(f"Session data for {user_id} is corrupted. No expiry time.")
            return None
        
        expiry_time = datetime.fromisoformat(expiry_time_str)
        
        if datetime.now() > expiry_time:
            logging.info(f"Session for user '{user_id}' has expired.")
            self.session_db.delete_session(session_token)
            return None
            
        logging.debug(f"Session validated for user '{user_id}'.")
        return user_id

    def end_session(self, session_token: str) -> str:
        """
        Ends a user's session by deleting the token.
        """
        self.session_db.delete_session(session_token)
        logging.info("Session ended.")
        return "Session ended successfully."
