# File location: vidya/security/api_key_manager.py

import logging
import os
import json
from vidya.security.encryption_service import EncryptionService
from vidya.config.configuration_manager import ConfigurationManager

class APIKeyManager:
    """
    Manages the secure storage and retrieval of API keys.
    """
    def __init__(self, encryption_service: EncryptionService, config_manager: ConfigurationManager):
        self.encryption_service = encryption_service
        self.config_manager = config_manager
        self.api_keys_file = self.config_manager.get('api_keys_file', 'vidya/config/api_keys.enc')
        self._load_keys()
        logging.info("APIKeyManager initialized.")

    def _load_keys(self):
        """Loads and decrypts API keys from the encrypted file."""
        self.keys = {}
        if os.path.exists(self.api_keys_file):
            try:
                with open(self.api_keys_file, 'rb') as f:
                    encrypted_data = f.read()
                decrypted_data = self.encryption_service.decrypt_data(encrypted_data)
                self.keys = json.loads(decrypted_data)
                logging.info("API keys loaded and decrypted.")
            except Exception as e:
                logging.error(f"Failed to load or decrypt API keys: {e}")

    def get_key(self, key_name: str) -> str | None:
        """Retrieves an API key by name."""
        return self.keys.get(key_name)

    def set_key(self, key_name: str, key_value: str):
        """Sets an API key and saves the encrypted keys to the file."""
        self.keys[key_name] = key_value
        self._save_keys()
        logging.info(f"API key '{key_name}' set successfully.")

    def _save_keys(self):
        """Encrypts and saves the API keys to a file."""
        try:
            json_data = json.dumps(self.keys)
            encrypted_data = self.encryption_service.encrypt_data(json_data)
            with open(self.api_keys_file, 'wb') as f:
                f.write(encrypted_data)
            logging.info("API keys encrypted and saved.")
        except Exception as e:
            logging.error(f"Failed to save API keys: {e}")
