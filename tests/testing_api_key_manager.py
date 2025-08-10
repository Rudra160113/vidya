# File location: vidya/tests/testing_api_key_manager.py

import logging
import os
import json
from vidya.tests.testing_framework import TestingFramework
from vidya.security.api_key_manager import APIKeyManager
from vidya.security.encryption_service import EncryptionService
from vidya.config.configuration_manager import ConfigurationManager

class TestingAPIKeyManager:
    """
    A suite of tests to verify the functionality of the APIKeyManager.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.config_file = "test_config.json"
        self.api_keys_file = "test_api_keys.enc"
        
        # Setup a mock config manager and encryption service for testing
        self.config_manager = ConfigurationManager(config_file=self.config_file)
        self.config_manager.config_data = {'api_keys_file': self.api_keys_file}
        self.encryption_service = EncryptionService(encryption_key="test_key_123")
        
        logging.info("TestingAPIKeyManager initialized.")

    def _cleanup_test_environment(self):
        """Removes test files after each test."""
        if os.path.exists(self.api_keys_file):
            os.remove(self.api_keys_file)
        if os.path.exists(self.config_file):
            os.remove(self.config_file)

    def test_key_set_and_get(self) -> bool:
        """Tests if an API key can be set and then retrieved correctly."""
        self._cleanup_test_environment()
        
        manager = APIKeyManager(self.encryption_service, self.config_manager)
        manager.set_key("openai", "sk-test-openai-key")
        retrieved_key = manager.get_key("openai")
        
        self._cleanup_test_environment()
        return retrieved_key == "sk-test-openai-key"

    def test_encrypted_storage(self) -> bool:
        """Tests if the API keys are stored in an encrypted format."""
        self._cleanup_test_environment()
        
        manager = APIKeyManager(self.encryption_service, self.config_manager)
        manager.set_key("openai", "sk-test-openai-key")
        
        if not os.path.exists(self.api_keys_file):
            return False
            
        with open(self.api_keys_file, 'rb') as f:
            encrypted_data = f.read()
            
        # Try to decrypt the data with a wrong key
        wrong_service = EncryptionService(encryption_key="wrong_key_123")
        try:
            wrong_service.decrypt_data(encrypted_data)
            decryption_failed = False
        except Exception:
            decryption_failed = True
            
        self._cleanup_test_environment()
        return decryption_failed

    def run_all_tests(self):
        """Runs all API key manager tests."""
        self.test_runner.run_test("Key Set and Get Test", self.test_key_set_and_get)
        self.test_runner.run_test("Encrypted Storage Test", self.test_encrypted_storage)
        self.test_runner.print_summary()
