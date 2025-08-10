# File location: vidya/user/user_profile.py

import logging
from vidya.services.supabase_handler import SupabaseHandler

class UserProfile:
    """
    Manages and stores user-specific data like preferences and current state.
    """
    def __init__(self, supabase_handler: SupabaseHandler):
        self.supabase_handler = supabase_handler
        logging.info("UserProfile initialized.")

    def get_user_preferences(self, user_id: str) -> dict:
        """
        Retrieves user preferences from the database.
        """
        try:
            # Assuming a 'profiles' table exists in your Supabase schema
            client = self.supabase_handler.get_next_client()
            if not client:
                return {}
            response = client.table('profiles').select('preferences').eq('user_id', user_id).execute()
            if response.data:
                return response.data[0]['preferences']
            return {}
        except Exception as e:
            logging.error(f"Error retrieving preferences for user {user_id}: {e}")
            return {}

    def update_user_preferences(self, user_id: str, new_preferences: dict) -> bool:
        """
        Updates user preferences in the database.
        """
        try:
            client = self.supabase_handler.get_next_client()
            if not client:
                return False
            client.table('profiles').update({'preferences': new_preferences}).eq('user_id', user_id).execute()
            logging.info(f"Preferences updated for user {user_id}.")
            return True
        except Exception as e:
            logging.error(f"Error updating preferences for user {user_id}: {e}")
            return False

    def get_user_state(self, user_id: str) -> dict:
        """
        Retrieves the current state or context for a user's session.
        This could be used to manage multi-turn conversations.
        """
        try:
            client = self.supabase_handler.get_next_client()
            if not client:
                return {}
            response = client.table('profiles').select('state').eq('user_id', user_id).execute()
            if response.data:
                return response.data[0]['state']
            return {}
        except Exception as e:
            logging.error(f"Error retrieving state for user {user_id}: {e}")
            return {}

    def update_user_state(self, user_id: str, new_state: dict) -> bool:
        """
        Updates the current state or context for a user's session.
        """
        try:
            client = self.supabase_handler.get_next_client()
            if not client:
                return False
            client.table('profiles').update({'state': new_state}).eq('user_id', user_id).execute()
            logging.info(f"State updated for user {user_id}.")
            return True
        except Exception as e:
            logging.error(f"Error updating state for user {user_id}: {e}")
            return False
