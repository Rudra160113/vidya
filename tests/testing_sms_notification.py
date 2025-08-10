# File location: vidya/tests/testing_sms_notification.py

import logging
import requests
from vidya.tests.testing_framework import TestingFramework
from vidya.services.sms_notification_service import SMSNotificationService
from vidya.config.configuration_manager import ConfigurationManager
from unittest.mock import patch, Mock

class TestingSMSNotification:
    """
    A suite of tests to verify the functionality of the SMSNotificationService.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.config_manager = ConfigurationManager()
        self.config_manager.config_data = {
            'sms_api_url': 'http://mock-sms-api.com/send',
            'sms_api_key': 'mock_api_key'
        }
        self.sms_service = SMSNotificationService(self.config_manager)
        logging.info("TestingSMSNotification initialized.")

    @patch('requests.post')
    def test_send_sms_success(self, mock_post: Mock) -> bool:
        """Tests if an SMS can be sent successfully via the API."""
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = self.sms_service.send_sms(
            recipient_number='+15551234567',
            message='Test message'
        )
        
        mock_post.assert_called_once()
        
        return result

    @patch('requests.post')
    def test_send_sms_failure(self, mock_post: Mock) -> bool:
        """Tests if the service handles an API request failure gracefully."""
        mock_post.side_effect = requests.exceptions.RequestException("API error")
        
        result = self.sms_service.send_sms(
            recipient_number='+15551234567',
            message='Test message'
        )
        
        return not result

    def run_all_tests(self):
        """Runs all SMS notification tests."""
        self.test_runner.run_test("Successful SMS Send Test", self.test_send_sms_success)
        self.test_runner.run_test("SMS Send Failure Test", self.test_send_sms_failure)
        self.test_runner.print_summary()
