# File location: vidya/services/user_profile_service.py

import logging
from vidya.database.database_service_supabase import DatabaseServiceSupabase
from vidya.core.dependency_injector import DependencyInjector

class UserProfileService:
    """
    Manages user profiles and their associated settings in the database.
    """
    def __init__(self, injector: DependencyInjector):
        self.db_service = injector.get(DatabaseServiceSupabase)
        self.table_name = "user_profiles"
        logging.info("UserProfileService initialized.")

    def get_user_profile(self, user_id: str) -> dict | None:
        """
        Fetches a user's profile from the database.
        
        Args:
            user_id (str): The unique identifier for the user.
            
        Returns:
            dict: The user's profile data, or None if not found.
        """
        if not self.db_service:
            return None
        
        result = self.db_service.fetch_records(self.table_name, filters={"user_id": user_id})
        
        if result and len(result) > 0:
            logging.info(f"Profile found for user '{user_id}'.")
            return result[0]
        else:
            logging.info(f"No profile found for user '{user_id}'.")
            return None

    def create_or_update_profile(self, user_id: str, profile_data: dict) -> bool:
        """
        Creates a new user profile or updates an existing one.
        
        Args:
            user_id (str): The unique identifier for the user.
            profile_data (dict): The data to be inserted or updated.
            
        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        if not self.db_service:
            return False
        
        profile_data['user_id'] = user_id
        
        # Supabase handles upserts, so we can just use the insert method
        result = self.db_service.insert_record(self.table_name, profile_data)
        
        if result:
            logging.info(f"Profile for user '{user_id}' created or updated successfully.")
            return True
        else:
            logging.error(f"Failed to create or update profile for user '{user_id}'.")
            return False
