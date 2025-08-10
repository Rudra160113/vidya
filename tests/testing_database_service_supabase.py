# File location: vidya/tests/testing_database_service_supabase.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.database.database_service_supabase import DatabaseServiceSupabase
from vidya.security.api_key_manager import APIKeyManager
from vidya.config.configuration_manager import ConfigurationManager

class TestingDatabaseServiceSupabase:
    """
    A suite of tests to verify the functionality of the DatabaseServiceSupabase.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.config_manager = ConfigurationManager()
        self.api_key_manager = APIKeyManager(unittest.mock.MagicMock(), self.config_manager)
        
        self.config_manager.config_data = {'supabase_url': 'mock_url'}
        unittest.mock.patch.object(APIKeyManager, 'get_key', return_value='mock_key').start()
        
        logging.info("TestingDatabaseServiceSupabase initialized.")

    @unittest.mock.patch('supabase.create_client')
    def test_insert_record_success(self, mock_create_client) -> bool:
        """Tests if a record can be inserted successfully."""
        # Mock the Supabase client and its methods
        mock_client = unittest.mock.Mock()
        mock_create_client.return_value = mock_client
        mock_client.from_.return_value.insert.return_value.execute.return_value.data = [{'id': 1, 'name': 'test'}]
        
        service = DatabaseServiceSupabase(self.config_manager, self.api_key_manager)
        result = service.insert_record('test_table', {'name': 'test'})
        
        mock_client.from_.assert_called_once_with('test_table')
        return result is not None and result[0]['id'] == 1

    @unittest.mock.patch('supabase.create_client')
    def test_fetch_records_with_filter(self, mock_create_client) -> bool:
        """Tests if records can be fetched with a filter."""
        # Mock the Supabase client and its methods
        mock_client = unittest.mock.Mock()
        mock_create_client.return_value = mock_client
        
        # Mock the query chain
        mock_query = unittest.mock.Mock()
        mock_query.select.return_value.eq.return_value.execute.return_value.data = [{'id': 1, 'name': 'test'}]
        mock_client.from_.return_value = mock_query
        
        service = DatabaseServiceSupabase(self.config_manager, self.api_key_manager)
        result = service.fetch_records('test_table', filters={'name': 'test'})
        
        mock_query.select.assert_called_once_with('*')
        mock_query.select.return_value.eq.assert_called_once_with('name', 'test')
        return len(result) == 1 and result[0]['name'] == 'test'

    def run_all_tests(self):
        """Runs all Supabase database service tests."""
        self.test_runner.run_test("Insert Record Test", self.test_insert_record_success)
        self.test_runner.run_test("Fetch Records With Filter Test", self.test_fetch_records_with_filter)
        self.test_runner.print_summary()
