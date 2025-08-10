# File location: vidya/utils/api_key_rotator.py

import logging
import uuid
from datetime import datetime, timedelta

class APIKeyRotator:
    """
    Manages the rotation of API keys to enhance security.
    """
    def __init__(self, rotation_interval_days: int = 90):
        self.rotation_interval = timedelta(days=rotation_interval_days)
        self.last_rotation = None
        self.current_keys = {}
        logging.info("APIKeyRotator initialized.")

    def rotate_key(self, key_name: str) -> str:
        """
        Generates a new key and updates the rotation timestamp.
        In a real scenario, this would involve invalidating the old key
        in the target service and updating the config.
        """
        new_key = str(uuid.uuid4())
        self.current_keys[key_name] = new_key
        self.last_rotation = datetime.now()
        logging.warning(f"New key for '{key_name}' generated: {new_key}. Old key would be invalidated.")
        return new_key

    def check_and_rotate(self, key_name: str) -> str:
        """
        Checks if a key needs to be rotated and performs the rotation if necessary.
        """
        if key_name not in self.current_keys or not self.last_rotation or \
           (datetime.now() - self.last_rotation) > self.rotation_interval:
            logging.info(f"Key '{key_name}' is old or missing. Initiating rotation.")
            return self.rotate_key(key_name)
        
        logging.info(f"Key '{key_name}' is still valid. No rotation needed.")
        return self.current_keys[key_name]
