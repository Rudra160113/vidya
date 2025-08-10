# File location: vidya/tests/testing_email_notification.py

import logging
import smtplib
from vidya.tests.testing_framework import TestingFramework
from vidya.services.email_notification_service import EmailNotificationService
from vidya.config.configuration_manager import ConfigurationManager
from unittest.mock import patch, Mock

class TestingEmailNotification:
    """
    A suite of tests to verify the functionality of the EmailNotificationService.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.config_manager = ConfigurationManager()
        self.config_manager.config_data = {
            'smtp_server': 'test_smtp',
            'smtp_port': 587,
            'smtp_user': 'test@test.com',
            'smtp_password': 'password123'
        }
        self.email_service = EmailNotificationService(self.config_manager)
        logging.info("TestingEmailNotification initialized.")

    @patch('smtplib.SMTP')
    def test_send_email_success(self, mock_smtp_class: Mock) -> bool:
        """Tests if an email can be sent successfully."""
        mock_server = mock_smtp_class.return_value.__enter__.return_value
        
        result = self.email_service.send_email(
            recipient='recipient@test.com',
            subject='Test Subject',
            body='Test Body'
        )
        
        # Verify that the server methods were called as expected
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with('test@test.com', 'password123')
        mock_server.send_message.assert_called_once()
        
        return result

    @patch('smtplib.SMTP')
    def test_send_email_failure(self, mock_smtp_class: Mock) -> bool:
        """Tests if the service handles a connection failure gracefully."""
        # Make the server login method raise an exception
        mock_server = mock_smtp_class.return_value.__enter__.return_value
        mock_server.login.side_effect = smtplib.SMTPAuthenticationError(535, "Auth Failed")
        
        result = self.email_service.send_email(
            recipient='recipient@test.com',
            subject='Test Subject',
            body='Test Body'
        )
        
        return not result

    def run_all_tests(self):
        """Runs all email notification tests."""
        self.test_runner.run_test("Successful Email Send Test", self.test_send_email_success)
        self.test_runner.run_test("Email Send Failure Test", self.test_send_email_failure)
        self.test_runner.print_summary()
