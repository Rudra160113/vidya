# File location: vidya/tests/integration_tests_supabase.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.nlp.command_parser import CommandParser
from vidya.core.command_executor import CommandExecutor
from vidya.database.database_service_supabase import DatabaseServiceSupabase
from vidya.core.dependency_injector import DependencyInjector
from vidya.core.command_router import CommandRouter
from vidya.core.plugin_manager import PluginManager
from vidya.security.api_key_manager import APIKeyManager
from vidya.config.configuration_manager import ConfigurationManager

class IntegrationTestsSupabase:
    """
    A suite of integration tests to verify the Supabase service works within the core flow.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup Dependency Injector and mock services
        self.injector = DependencyInjector()
        self.mock_api_key_manager = unittest.mock.Mock(spec=APIKeyManager)
        self.mock_config_manager = unittest.mock.Mock(spec=ConfigurationManager)
        self.mock_database_service = DatabaseServiceSupabase(self.mock_config_manager, self.mock_api_key_manager)
        self.mock_command_router = CommandRouter()
        self.mock_plugin_manager = unittest.mock.Mock(spec=PluginManager)

        self.injector.register(DatabaseServiceSupabase, self.mock_database_service)
        self.injector.register(CommandRouter, self.mock_command_router)
        self.injector.register('plugin_manager', self.mock_plugin_manager)

        self.parser = CommandParser()
        self.executor = CommandExecutor(self.injector)
        
        logging.info("Supabase Integration Test Suite initialized.")
    
    @unittest.mock.patch.object(DatabaseServiceSupabase, 'insert_record', return_value=[{'id': 1}])
    @unittest.mock.patch.object(DatabaseServiceSupabase, 'fetch_records', return_value=[{'id': 1, 'setting': 'dark_mode', 'value': True}])
    def test_database_save_and_load_flow(self, mock_fetch, mock_insert) -> bool:
        """
        Simulates a workflow of saving and then loading data from the database.
        """
        # Define a mock handler that uses the database service
        def save_setting_handler(args):
            return self.mock_database_service.insert_record("settings", args)

        def get_setting_handler(args):
            return self.mock_database_service.fetch_records("settings", {"setting": args.get("setting")})
            
        # Register the mock handlers with the router
        self.mock_command_router.register_handler("save_setting", save_setting_handler)
        self.mock_command_router.register_handler("get_setting", get_setting_handler)
        
        # Step 1: Simulate saving a setting
        save_nlp_output = {
            'text': 'save dark mode preference',
            'entities': {'command': 'save_setting', 'setting': 'dark_mode', 'value': True}
        }
        save_command = self.parser.parse_nlp_output(save_nlp_output)
        save_result = self.executor.execute_command(save_command)
        
        # Step 2: Simulate getting the setting
        get_nlp_output = {
            'text': 'get dark mode preference',
            'entities': {'command': 'get_setting', 'setting': 'dark_mode'}
        }
        get_command = self.parser.parse_nlp_output(get_nlp_output)
        get_result = self.executor.execute_command(get_command)
        
        # Verify that the database methods were called and results are correct
        mock_insert.assert_called_once_with("settings", {'setting': 'dark_mode', 'value': True})
        mock_fetch.assert_called_once_with("settings", {'setting': 'dark_mode'})
        
        is_result_correct = get_result[0]['setting'] == 'dark_mode' and get_result[0]['value'] == True
        
        return is_result_correct

    def run_all_tests(self):
        """Runs all integration tests."""
        self.test_runner.run_test("Supabase Save/Load Flow Test", self.test_database_save_and_load_flow)
        self.test_runner.print_summary()
