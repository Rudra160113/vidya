# File location: vidya/config/vidya_settings.py

import json
import os
import logging

class VidyaSettings:
    """
    Manages and loads application settings from a JSON file.
    """
    def __init__(self, settings_file: str = 'vidya/config/settings.json'):
        self.settings_file = settings_file
        self.settings = self._load_settings()
        logging.info("VidyaSettings initialized.")

    def _load_settings(self):
        """Loads settings from the JSON file."""
        if not os.path.exists(self.settings_file):
            logging.error(f"Settings file not found at '{self.settings_file}'. Creating a default file.")
            self._create_default_settings()
            return {}
        
        try:
            with open(self.settings_file, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError as e:
            logging.error(f"Error decoding settings JSON file: {e}")
            return {}

    def _create_default_settings(self):
        """Creates a default settings file with placeholder values."""
        default_settings = {
            "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY_HERE",
            "HUGGINGFACE_API_KEY": "YOUR_HUGGINGFACE_API_KEY_HERE",
            "EMAIL_ADDRESS": "YOUR_EMAIL_ADDRESS@example.com",
            "EMAIL_PASSWORD": "YOUR_APP_SPECIFIC_PASSWORD_HERE",
            "DEFAULT_CRAWL_URL": "https://www.example.com",
            "CRAWL_MAX_DEPTH": 2,
            "LOG_LEVEL": "INFO"
        }
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(default_settings, f, indent=4)
            logging.info("Default settings file created.")
        except Exception as e:
            logging.error(f"Failed to create default settings file: {e}")

    def get(self, key, default=None):
        """Retrieves a setting value by key."""
        return self.settings.get(key, default)

    def set(self, key, value):
        """Sets a setting value and saves it to the file."""
        self.settings[key] = value
        try:
            with open(self.settings_file, 'w') as f:
                json.dump(self.settings, f, indent=4)
            logging.info(f"Setting '{key}' updated successfully.")
        except Exception as e:
            logging.error(f"Failed to save settings: {e}")

# This is the actual JSON file that would live at `vidya/config/settings.json`
# You would need to create this file manually.

# vidya/config/settings.json
# {
#   "GEMINI_API_KEY": "YOUR_GEMINI_API_KEY_HERE",
#   "HUGGINGFACE_API_KEY": "YOUR_HUGGINGFACE_API_KEY_HERE",
#   "EMAIL_ADDRESS": "YOUR_EMAIL_ADDRESS@example.com",
#   "EMAIL_PASSWORD": "YOUR_APP_SPECIFIC_PASSWORD_HERE",
#   "DEFAULT_CRAWL_URL": "https://www.example.com",
#   "CRAWL_MAX_DEPTH": 2,
#   "LOG_LEVEL": "INFO"
# }
