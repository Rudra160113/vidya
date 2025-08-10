# File location: vidya/user/voice_profile.py

import logging
from vidya.data.database_connector import DatabaseConnector

class VoiceProfile:
    """
    Manages and stores voice-specific data for user identification and personalization.
    """
    def __init__(self, db_connector: DatabaseConnector):
        self.db_connector = db_connector
        logging.info("VoiceProfile initialized.")
        self._setup_table()

    def _setup_table(self):
        """Creates the voice_profiles table if it doesn't exist."""
        create_table = """
        CREATE TABLE IF NOT EXISTS voice_profiles (
            user_id TEXT PRIMARY KEY,
            voice_data BLOB NOT NULL
        );
        """
        self.db_connector.execute_query(create_table)
        logging.info("Voice profile table verified/created.")

    def save_voice_data(self, user_id: str, audio_data) -> str:
        """
        Saves a user's voice data to the database.
        `audio_data` would be a binary representation of the voice sample.
        """
        try:
            # Check if a profile already exists
            query = "SELECT EXISTS(SELECT 1 FROM voice_profiles WHERE user_id=?)"
            exists = self.db_connector.execute_query(query, (user_id,))
            
            if exists and exists[0][0]:
                update_query = "UPDATE voice_profiles SET voice_data=? WHERE user_id=?"
                self.db_connector.execute_query(update_query, (audio_data, user_id))
                return f"Voice profile for '{user_id}' updated."
            else:
                insert_query = "INSERT INTO voice_profiles (user_id, voice_data) VALUES (?, ?)"
                self.db_connector.execute_query(insert_query, (user_id, audio_data))
                return f"Voice profile for '{user_id}' created."
        except Exception as e:
            logging.error(f"Failed to save voice data for '{user_id}': {e}")
            return "An error occurred while saving the voice profile."
