# File location: vidya/tests/testing_http_client.py

import logging
import unittest.mock
import requests
from vidya.tests.testing_framework import TestingFramework
from vidya.utils.http_client import HttpClient

class TestingHttpClient:
    """
    A suite of tests to verify the functionality of the HttpClient.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.client = HttpClient()
        logging.info("TestingHttpClient initialized.")
    
    @unittest.mock.patch('requests.get')
    def test_get_request_success(self, mock_get) -> bool:
        """Tests a successful GET request."""
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'status': 'ok'}
        mock_get.return_value = mock_response
        
        response, status = self.client.get('http://test.com/api')
        
        return status == 200 and response['status'] == 'ok'

    @unittest.mock.patch('requests.post')
    def test_post_request_success(self, mock_post) -> bool:
        """Tests a successful POST request."""
        mock_response = unittest.mock.Mock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'status': 'created'}
        mock_post.return_value = mock_response
        
        response, status = self.client.post('http://test.com/api', data={'key': 'value'})
        
        return status == 201 and response['status'] == 'created'

    @unittest.mock.patch('requests.get', side_effect=requests.exceptions.Timeout)
    def test_request_timeout(self, mock_get) -> bool:
        """Tests if the client handles a timeout error."""
        response, status = self.client.get('http://test.com/api')
        
        return status == 408 and response is None

    def run_all_tests(self):
        """Runs all HTTP client tests."""
        self.test_runner.run_test("GET Request Success Test", self.test_get_request_success)
        self.test_runner.run_test("POST Request Success Test", self.test_post_request_success)
        self.test_runner.run_test("Request Timeout Test", self.test_request_timeout)
        self.test_runner.print_summary()
