# File location: vidya/config/configuration_manager.py

import logging
import json
import os

class ConfigurationManager:
    """
    Loads and provides application configuration settings.
    """
    def __init__(self, config_file: str = 'vidya/config/config.json'):
        self.config_data = {}
        self.config_file = config_file
        self._load_config()
        logging.info("ConfigurationManager initialized.")
        
    def _load_config(self):
        """Loads configuration data from a JSON file and environment variables."""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.config_data = json.load(f)
                logging.info(f"Configuration loaded from '{self.config_file}'.")
            except Exception as e:
                logging.error(f"Failed to load config file: {e}")
        else:
            logging.warning(f"Config file '{self.config_file}' not found. Using default/environment settings.")

        # Override with environment variables for production flexibility
        self._load_env_vars()
        
    def _load_env_vars(self):
        """Overrides configuration settings with environment variables."""
        # Example: set the API key from an environment variable if it exists
        if 'VIDYA_API_KEY' in os.environ:
            self.config_data['api_key'] = os.environ['VIDYA_API_KEY']
            logging.info("API key loaded from environment variable.")

    def get(self, key: str, default=None):
        """
        Retrieves a configuration value by its key.
        """
        return self.config_data.get(key, default)
