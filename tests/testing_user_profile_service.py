# File location: vidya/tests/testing_user_profile_service.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.services.user_profile_service import UserProfileService
from vidya.database.database_service_supabase import DatabaseServiceSupabase
from vidya.core.dependency_injector import DependencyInjector

class TestingUserProfileService:
    """
    A suite of tests to verify the functionality of the UserProfileService.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup Dependency Injector with a mock database service
        self.injector = DependencyInjector()
        self.mock_db_service = unittest.mock.Mock(spec=DatabaseServiceSupabase)
        self.injector.register(DatabaseServiceSupabase, self.mock_db_service)
        
        self.service = UserProfileService(self.injector)
        logging.info("TestingUserProfileService initialized.")
    
    def test_get_user_profile_found(self) -> bool:
        """Tests fetching a user profile that exists."""
        self.mock_db_service.fetch_records.return_value = [{'user_id': 'test_user', 'setting': 'theme', 'value': 'light'}]
        
        profile = self.service.get_user_profile('test_user')
        
        self.mock_db_service.fetch_records.assert_called_once_with('user_profiles', filters={'user_id': 'test_user'})
        
        return profile is not None and profile['user_id'] == 'test_user'

    def test_get_user_profile_not_found(self) -> bool:
        """Tests fetching a user profile that does not exist."""
        self.mock_db_service.fetch_records.return_value = []
        
        profile = self.service.get_user_profile('non_existent_user')
        
        self.mock_db_service.fetch_records.assert_called_once_with('user_profiles', filters={'user_id': 'non_existent_user'})
        
        return profile is None

    def test_create_or_update_profile_success(self) -> bool:
        """Tests creating/updating a user profile successfully."""
        self.mock_db_service.insert_record.return_value = [{'user_id': 'new_user', 'setting': 'theme', 'value': 'dark'}]
        
        success = self.service.create_or_update_profile('new_user', {'setting': 'theme', 'value': 'dark'})
        
        self.mock_db_service.insert_record.assert_called_once_with('user_profiles', {'user_id': 'new_user', 'setting': 'theme', 'value': 'dark'})
        
        return success

    def run_all_tests(self):
        """Runs all user profile service tests."""
        self.test_runner.run_test("Get Profile Found Test", self.test_get_user_profile_found)
        self.test_runner.run_test("Get Profile Not Found Test", self.test_get_user_profile_not_found)
        self.test_runner.run_test("Create/Update Profile Success Test", self.test_create_or_update_profile_success)
        self.test_runner.print_summary()
