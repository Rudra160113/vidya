# File location: vidya/tests/testing_security_manager.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.security.security_manager import SecurityManager

class TestingSecurityManager:
    """
    A suite of tests to verify the functionality of the SecurityManager.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.manager = SecurityManager()
        logging.info("TestingSecurityManager initialized.")
    
    def test_password_hashing_and_verification(self) -> bool:
        """Tests if a password can be hashed and then verified successfully."""
        password = "mysecurepassword123"
        hashed_password = self.manager.hash_password(password)
        
        is_verified = self.manager.verify_password(password, hashed_password)
        is_wrong_password_verified = self.manager.verify_password("wrong_password", hashed_password)
        
        return is_verified and not is_wrong_password_verified

    def test_data_encryption_and_decryption(self) -> bool:
        """Tests if data can be encrypted and then decrypted back to its original form."""
        plain_text = "This is a secret message."
        encrypted_text = self.manager.encrypt_data(plain_text)
        decrypted_text = self.manager.decrypt_data(encrypted_text)
        
        return plain_text == decrypted_text and plain_text != encrypted_text

    def run_all_tests(self):
        """Runs all security manager tests."""
        self.test_runner.run_test("Password Hashing Test", self.test_password_hashing_and_verification)
        self.test_runner.run_test("Data Encryption Test", self.test_data_encryption_and_decryption)
        self.test_runner.print_summary()
