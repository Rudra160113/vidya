# File location: vidya/tests/testing_encryption_service.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.security.encryption_service import EncryptionService

class TestingEncryptionService:
    """
    A suite of tests to verify the functionality of the EncryptionService.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.encryption_service = EncryptionService(encryption_key="test_secure_key")
        logging.info("TestingEncryptionService initialized.")

    def test_encryption_decryption_cycle(self) -> bool:
        """Tests if data can be encrypted and then decrypted back to its original form."""
        original_data = "This is a secret message."
        
        encrypted_data = self.encryption_service.encrypt_data(original_data)
        decrypted_data = self.encryption_service.decrypt_data(encrypted_data)
        
        return original_data == decrypted_data

    def test_tampered_data_fails_decryption(self) -> bool:
        """Tests if a tampered encrypted message fails decryption."""
        original_data = "This is a secret message."
        encrypted_data = self.encryption_service.encrypt_data(original_data)
        
        # Tamper with a single byte of the encrypted data
        tampered_data = encrypted_data[:-1] + b'X'
        
        try:
            self.encryption_service.decrypt_data(tampered_data)
            decryption_failed = False
        except Exception:
            decryption_failed = True
            
        return decryption_failed

    def run_all_tests(self):
        """Runs all encryption service tests."""
        self.test_runner.run_test("Encryption-Decryption Cycle Test", self.test_encryption_decryption_cycle)
        self.test_runner.run_test("Tampered Data Decryption Test", self.test_tampered_data_fails_decryption)
        self.test_runner.print_summary()
