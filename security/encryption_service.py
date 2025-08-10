# File location: vidya/security/encryption_service.py

import logging
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
import os

class EncryptionService:
    """
    Provides data encryption and decryption services using a symmetric key.
    """
    def __init__(self, encryption_key: str):
        self.encryption_key = encryption_key
        # Derive a key from the provided string using PBKDF2
        password = encryption_key.encode()
        salt = b'vidya_ai_salt'  # In a real app, this should be unique per key
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=default_backend()
        )
        derived_key = base64.urlsafe_b64encode(kdf.derive(password))
        self.fernet = Fernet(derived_key)
        logging.info("EncryptionService initialized.")

    def encrypt_data(self, data: str) -> bytes:
        """
        Encrypts a string of data.
        """
        return self.fernet.encrypt(data.encode())

    def decrypt_data(self, encrypted_data: bytes) -> str:
        """
        Decrypts a bytes object of data.
        """
        return self.fernet.decrypt(encrypted_data).decode()
