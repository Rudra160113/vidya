# File location: vidya/core/session_manager.py

import logging
import uuid
import datetime
from vidya.user.user_profile import UserProfile

class SessionManager:
    """
    Manages user sessions, including creation, state tracking, and termination.
    """
    def __init__(self, user_profile: UserProfile):
        self.user_profile = user_profile
        self.active_sessions = {}  # In-memory dictionary to track active sessions
        logging.info("SessionManager initialized.")

    def create_session(self, user_id: str) -> str:
        """
        Creates a new session for a user and returns a unique session ID.
        """
        session_id = str(uuid.uuid4())
        session_data = {
            "user_id": user_id,
            "start_time": datetime.datetime.now(),
            "last_interaction": datetime.datetime.now(),
            "context": {},
            "active": True
        }
        self.active_sessions[session_id] = session_data
        logging.info(f"New session created for user '{user_id}' with ID '{session_id}'.")
        return session_id

    def update_session(self, session_id: str, new_context: dict):
        """
        Updates the context and last interaction time for an active session.
        """
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['last_interaction'] = datetime.datetime.now()
            self.active_sessions[session_id]['context'].update(new_context)
            # You could also persist this to the database here if needed
            self.user_profile.update_user_state(
                self.active_sessions[session_id]['user_id'],
                self.active_sessions[session_id]['context']
            )
            logging.info(f"Session '{session_id}' updated.")
            return True
        logging.warning(f"Attempted to update a non-existent session: {session_id}")
        return False
        
    def get_session_context(self, session_id: str) -> dict:
        """
        Retrieves the current context for a given session.
        """
        if session_id in self.active_sessions:
            return self.active_sessions[session_id]['context']
        logging.warning(f"Attempted to get context from a non-existent session: {session_id}")
        return {}

    def end_session(self, session_id: str) -> bool:
        """
        Ends an active session.
        """
        if session_id in self.active_sessions:
            del self.active_sessions[session_id]
            logging.info(f"Session '{session_id}' ended.")
            return True
        logging.warning(f"Attempted to end a non-existent session: {session_id}")
        return False
