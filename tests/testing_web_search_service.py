# File location: vidya/tests/testing_web_search_service.py

import logging
import requests
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.services.web_search_service import WebSearchService
from vidya.config.configuration_manager import ConfigurationManager

class TestingWebSearchService:
    """
    A suite of tests to verify the functionality of the WebSearchService.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.config_manager = ConfigurationManager()
        self.web_search_service = WebSearchService(self.config_manager)
        logging.info("TestingWebSearchService initialized.")

    @unittest.mock.patch('requests.get')
    def test_successful_search(self, mock_get) -> bool:
        """Tests if a successful search returns parsed results."""
        # Mock the HTTP response with a sample HTML snippet
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = """
        <html><body>
        <div class="g">
            <h3><a href="http://example.com/result1">Result 1 Title</a></h3>
        </div>
        <div class="g">
            <h3><a href="http://example.com/result2">Result 2 Title</a></h3>
        </div>
        </body></html>
        """
        mock_get.return_value = mock_response
        
        query = "test search"
        results = self.web_search_service.search(query)
        
        # Verify that the correct URL was called
        mock_get.assert_called_once_with(
            unittest.mock.ANY,
            headers=unittest.mock.ANY,
            timeout=unittest.mock.ANY
        )
        
        # Check if the results were parsed correctly
        return len(results) == 2 and results[0]['title'] == "Result 1 Title"

    @unittest.mock.patch('requests.get', side_effect=requests.exceptions.RequestException("Network Error"))
    def test_failed_search(self, mock_get) -> bool:
        """Tests if a failed search returns an empty list."""
        query = "another test"
        results = self.web_search_service.search(query)
        
        return len(results) == 0

    def run_all_tests(self):
        """Runs all web search service tests."""
        self.test_runner.run_test("Successful Search Test", self.test_successful_search)
        self.test_runner.run_test("Failed Search Test", self.test_failed_search)
        self.test_runner.print_summary()
