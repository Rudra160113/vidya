# File location: vidya/tests/testing_configuration_manager.py

import logging
import os
import json
from vidya.tests.testing_framework import TestingFramework
from vidya.utils.testing_utility import TestingUtility
from vidya.config.configuration_manager import ConfigurationManager

class TestingConfigurationManager:
    """
    A suite of tests to verify the functionality of the ConfigurationManager.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.config_file_path = "test_config.json"
        logging.info("TestingConfigurationManager initialized.")

    def _setup_test_environment(self):
        """Sets up a mock config file and an environment variable for testing."""
        config_data = {
            "api_key": "file_api_key_123",
            "db_host": "localhost"
        }
        TestingUtility.create_dummy_config_file(self.config_file_path, json.dumps(config_data))
        os.environ['VIDYA_API_KEY'] = "env_api_key_456"

    def _cleanup_test_environment(self):
        """Removes the mock config file and the environment variable."""
        TestingUtility.cleanup_file(self.config_file_path)
        if 'VIDYA_API_KEY' in os.environ:
            del os.environ['VIDYA_API_KEY']

    def test_file_loading(self) -> bool:
        """Tests if the configuration manager loads settings from the config file."""
        self._setup_test_environment()
        manager = ConfigurationManager(config_file=self.config_file_path)
        self._cleanup_test_environment()
        
        # The env var should override the file, but we'll check both
        return manager.get("db_host") == "localhost"

    def test_environment_variable_override(self) -> bool:
        """Tests if an environment variable correctly overrides a file setting."""
        self._setup_test_environment()
        manager = ConfigurationManager(config_file=self.config_file_path)
        self._cleanup_test_environment()
        
        # The environment variable should take precedence
        return manager.get("api_key") == "env_api_key_456"

    def run_all_tests(self):
        """Runs all configuration manager tests."""
        self.test_runner.run_test("File Loading Test", self.test_file_loading)
        self.test_runner.run_test("Environment Variable Override Test", self.test_environment_variable_override)
        self.test_runner.print_summary()
