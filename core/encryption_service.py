# File location: vidya/core/encryption_service.py

import logging
from cryptography.fernet import Fernet
import base64

class EncryptionService:
    """
    Provides symmetric encryption and decryption for sensitive data.
    """
    def __init__(self, encryption_key: str):
        # The key must be a URL-safe base64-encoded 32-byte key.
        try:
            self.key = base64.urlsafe_b64encode(encryption_key.encode('utf-8').ljust(32)[:32])
            self.cipher_suite = Fernet(self.key)
            logging.info("EncryptionService initialized.")
        except Exception as e:
            logging.error(f"Failed to initialize EncryptionService: {e}")
            self.cipher_suite = None

    def encrypt(self, data: str) -> str:
        """
        Encrypts a string of data.
        """
        if not self.cipher_suite:
            return "Encryption service is not active."
        
        try:
            encrypted_data = self.cipher_suite.encrypt(data.encode('utf-8'))
            return encrypted_data.decode('utf-8')
        except Exception as e:
            logging.error(f"Failed to encrypt data: {e}")
            return ""

    def decrypt(self, encrypted_data: str) -> str:
        """
        Decrypts a string of data.
        """
        if not self.cipher_suite:
            return "Encryption service is not active."
            
        try:
            decrypted_data = self.cipher_suite.decrypt(encrypted_data.encode('utf-8'))
            return decrypted_data.decode('utf-8')
        except Exception as e:
            logging.error(f"Failed to decrypt data: {e}")
            return ""
