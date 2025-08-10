# File location: vidya/tests/testing_plugin_command_handlers.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.plugins import plugin_command_handlers
from vidya.services.web_search_service import WebSearchService
from vidya.services.user_profile_service import UserProfileService
from vidya.core.dependency_injector import DependencyInjector

class TestingPluginCommandHandlers:
    """
    A suite of tests to verify the functionality of the example plugin handlers.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup Dependency Injector with mock services
        self.injector = DependencyInjector()
        self.mock_web_search_service = unittest.mock.Mock(spec=WebSearchService)
        self.mock_user_profile_service = unittest.mock.Mock(spec=UserProfileService)
        
        self.injector.register(WebSearchService, self.mock_web_search_service)
        self.injector.register(UserProfileService, self.mock_user_profile_service)
        
        logging.info("TestingPluginCommandHandlers initialized.")

    def test_handle_web_search_success(self) -> bool:
        """Tests if the web search handler works correctly with a successful result."""
        self.mock_web_search_service.search.return_value = [
            {'title': 'Result 1', 'url': 'http://result1.com'},
            {'title': 'Result 2', 'url': 'http://result2.com'}
        ]
        
        args = {'query': 'test query'}
        result = plugin_command_handlers.handle_web_search(self.injector, args)
        
        self.mock_web_search_service.search.assert_called_once_with('test query')
        
        return "Result 1" in result and "http://result2.com" in result

    def test_handle_web_search_no_results(self) -> bool:
        """Tests if the web search handler handles no results correctly."""
        self.mock_web_search_service.search.return_value = []
        
        args = {'query': 'no results'}
        result = plugin_command_handlers.handle_web_search(self.injector, args)
        
        return "couldn't find any results" in result

    def test_handle_get_profile_found(self) -> bool:
        """Tests if the get profile handler works correctly for an existing profile."""
        self.mock_user_profile_service.get_user_profile.return_value = {'user_id': 'test_user', 'theme': 'dark'}
        
        args = {'user_id': 'test_user'}
        result = plugin_command_handlers.handle_get_profile(self.injector, args)
        
        self.mock_user_profile_service.get_user_profile.assert_called_once_with('test_user')
        
        return "theme: dark" in result

    def test_handle_get_profile_not_found(self) -> bool:
        """Tests if the get profile handler handles a missing profile correctly."""
        self.mock_user_profile_service.get_user_profile.return_value = None
        
        args = {'user_id': 'non_existent_user'}
        result = plugin_command_handlers.handle_get_profile(self.injector, args)
        
        return "couldn't find a profile" in result

    def run_all_tests(self):
        """Runs all plugin command handler tests."""
        self.test_runner.run_test("Web Search Success Test", self.test_handle_web_search_success)
        self.test_runner.run_test("Web Search No Results Test", self.test_handle_web_search_no_results)
        self.test_runner.run_test("Get Profile Found Test", self.test_handle_get_profile_found)
        self.test_runner.run_test("Get Profile Not Found Test", self.test_handle_get_profile_not_found)
        self.test_runner.print_summary()
