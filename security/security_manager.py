# File location: vidya/security/security_manager.py

import logging
import bcrypt
import base64
import os
from cryptography.fernet import Fernet
from vidya.config.configuration_manager import ConfigurationManager

class SecurityManager:
    """
    A centralized service for handling security-related tasks like
    password hashing, data encryption, and key management.
    """
    def __init__(self, config_manager: ConfigurationManager):
        self.config_manager = config_manager
        self._encryption_key = self._get_encryption_key()
        self._fernet = Fernet(self._encryption_key)
        logging.info("SecurityManager initialized.")

    def _get_encryption_key(self) -> bytes:
        """
        Retrieves or generates the encryption key.
        In a production environment, this key should be stored securely.
        """
        key_str = self.config_manager.get('encryption_key')
        if not key_str:
            logging.warning("Encryption key not found in config. Generating a new one.")
            key = Fernet.generate_key()
            # For demonstration, we'll store it. In reality, this would be a manual step.
            self.config_manager.set('encryption_key', key.decode('utf-8'))
            return key
        
        return key_str.encode('utf-8')

    def hash_password(self, password: str) -> str:
        """Hashes a password for secure storage."""
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        return hashed.decode('utf-8')

    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifies a password against a stored hash."""
        try:
            return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
        except Exception as e:
            logging.error(f"Error verifying password: {e}")
            return False

    def encrypt_data(self, data: str) -> str:
        """Encrypts data using the configured key."""
        encrypted = self._fernet.encrypt(data.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted).decode('utf-8')

    def decrypt_data(self, encrypted_data: str) -> str | None:
        """Decrypts data using the configured key."""
        try:
            encrypted = base64.urlsafe_b64decode(encrypted_data)
            decrypted = self._fernet.decrypt(encrypted)
            return decrypted.decode('utf-8')
        except Exception as e:
            logging.error(f"Error decrypting data: {e}")
            return None
