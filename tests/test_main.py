# File location: vidya/tests/test_main.py

import unittest
import os
import sys
from unittest.mock import MagicMock, patch

# Add the parent directory to the path so we can import from `vidya`
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.main import main
from core.vidya_brain import VidyaBrain
from services.supabase_handler import SupabaseHandler
from services.email_handler import EmailHandler

class TestVidyaCore(unittest.TestCase):
    """
    Unit tests for the core components of the Vidya AI assistant.
    """
    
    @patch('builtins.input', side_effect=['test_user', 'exit'])
    @patch('core.main.VidyaBrain')
    @patch('core.main.SupabaseHandler')
    @patch('core.main.EmailHandler')
    @patch('core.main.AutoStart')
    @patch('core.main.PermissionHandler')
    @patch('core.main.WebCrawler')
    def test_main_initialization_and_exit(self, mock_webcrawler, mock_permission_handler, mock_autostart, mock_email_handler, mock_supabase_handler, mock_vidya_brain, mock_input):
        """Test if the main function initializes components and exits correctly."""
        # Mocking the initialization of all dependent classes
        mock_supabase_handler.return_value = MagicMock()
        mock_email_handler.return_value = MagicMock()
        mock_vidya_brain.return_value = MagicMock()

        # Run the main function
        with self.assertRaises(SystemExit):
            main()

        # Assert that all components were initialized
        mock_supabase_handler.assert_called_once_with('vidya/config/supabase_config.json')
        mock_email_handler.assert_called_once()
        mock_vidya_brain.assert_called_once()
        mock_webcrawler.assert_called_once()

    @patch('core.vidya_brain.VidyaBrain._get_gemini_response')
    def test_vidya_brain_response_generation(self, mock_gemini_response):
        """Test if VidyaBrain correctly processes input and generates a response."""
        mock_gemini_response.return_value = "Mocked AI response."

        mock_supabase_handler = MagicMock()
        mock_supabase_handler.get_history.return_value = []
        mock_supabase_handler.search_crawled_data.return_value = []
        mock_email_handler = MagicMock()
        
        brain = VidyaBrain("mock_gemini_key", "mock_hf_key", mock_supabase_handler, mock_email_handler)
        response = brain.process_input("hello", "test_user_1")

        self.assertEqual(response, "Mocked AI response.")
        mock_gemini_response.assert_called_once()
        mock_supabase_handler.log_interaction.assert_called()

if __name__ == '__main__':
    unittest.main()
