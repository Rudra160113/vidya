# File location: vidya/tests/testing_mock_data.py

class TestingMockData:
    """
    Provides mock data for testing various components of the Vidya application.
    """
    @staticmethod
    def get_mock_user_profile():
        """Returns a mock user profile dictionary."""
        return {
            "user_id": "test_user_123",
            "name": "Test User",
            "email": "test@example.com",
            "preferences": "{'theme': 'dark'}"
        }
        
    @staticmethod
    def get_mock_email():
        """Returns a mock email object."""
        return {
            "from": "sender@example.com",
            "to": "test@example.com",
            "subject": "Test Email",
            "body": "This is a test email body."
        }
        
    @staticmethod
    def get_mock_command():
        """Returns a mock command dictionary."""
        return {
            "text": "send an email to test@example.com with subject 'Test' and body 'Hello'",
            "user_id": "test_user_123"
        }
        
    @staticmethod
    def get_mock_analytics_event():
        """Returns a mock analytics event dictionary."""
        return {
            "event_type": "command_execution",
            "event_data": {"command": "open browser"}
        }
