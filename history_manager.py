# File location: vidya/history_manager.py

import logging
from vidya.services.supabase_handler import SupabaseHandler
import datetime

class HistoryManager:
    """
    Manages the storage, retrieval, and analysis of user conversation history.
    """
    def __init__(self, supabase_handler: SupabaseHandler):
        self.supabase_handler = supabase_handler
        logging.info("HistoryManager initialized.")
        
    def add_entry(self, user_id: str, source: str, message: str):
        """
        Adds a new interaction entry to the user's history in the database.
        """
        return self.supabase_handler.log_interaction(user_id, source, message)

    def get_history(self, user_id: str) -> str:
        """
        Retrieves and formats a user's full conversation history from all databases.
        """
        history = self.supabase_handler.get_history(user_id)
        if not history:
            return "No history found for this user."
        
        formatted_history = ""
        for record in history:
            # Assuming 'created_at', 'source', and 'message' are keys in the record
            timestamp = datetime.datetime.fromisoformat(record.get('created_at')).strftime("%Y-%m-%d %H:%M:%S")
            source = record.get('source')
            message = record.get('message')
            formatted_history += f"[{timestamp}] {source}: {message}\n"
            
        return formatted_history
        
    def clear_history(self, user_id: str) -> str:
        """
        Deletes all history entries for a specific user.
        Note: The SupabaseHandler would need a corresponding method to handle this.
        """
        logging.warning(f"User {user_id} requested history deletion. This is a permanent action.")
        # Placeholder for a method to delete history from Supabase
        # result = self.supabase_handler.delete_history(user_id)
        # if result:
        #    return "Your history has been successfully cleared."
        # else:
        #    return "An error occurred while trying to clear your history."
        return "History clearing functionality is not yet implemented."
