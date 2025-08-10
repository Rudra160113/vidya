# File location: vidya/config/api_key_manager.py

import os
import logging
from vidya.config.vidya_settings import VidyaSettings

class APIKeyManager:
    """
    A secure manager for retrieving API keys from environment variables or a settings file.
    """
    def __init__(self, settings: VidyaSettings):
        self.settings = settings
        logging.info("APIKeyManager initialized.")

    def get_key(self, key_name: str) -> str:
        """
        Retrieves an API key, first from environment variables, then from the settings file.
        """
        # First, try to get the key from environment variables
        env_key = os.environ.get(key_name)
        if env_key:
            logging.info(f"Retrieved key '{key_name}' from environment variable.")
            return env_key

        # If not found, try to get it from the settings file
        settings_key = self.settings.get(key_name)
        if settings_key and settings_key != f"YOUR_{key_name}_HERE":
            logging.warning(f"Retrieved key '{key_name}' from settings file. Consider using environment variables for better security.")
            return settings_key

        # If still not found or is the placeholder, raise an error
        logging.error(f"API key '{key_name}' not found in environment variables or settings file.")
        raise ValueError(f"API key '{key_name}' is not set. Please configure it in your environment or settings file.")
