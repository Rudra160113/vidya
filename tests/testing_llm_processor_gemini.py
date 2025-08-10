# File location: vidya/tests/testing_llm_processor_gemini.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.llm.llm_processor_gemini import LLMProcessorGemini
from vidya.security.api_key_manager import APIKeyManager
from vidya.config.configuration_manager import ConfigurationManager

class TestingLLMProcessorGemini:
    """
    A suite of tests to verify the functionality of the LLMProcessorGemini.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.config_manager = ConfigurationManager()
        self.api_key_manager = APIKeyManager(unittest.mock.MagicMock(), self.config_manager)
        
        logging.info("TestingLLMProcessorGemini initialized.")

    @unittest.mock.patch('google.generativeai.GenerativeModel')
    @unittest.mock.patch.object(APIKeyManager, 'get_key', return_value='mock-gemini-key')
    def test_generate_response_success(self, mock_get_key, mock_generative_model) -> bool:
        """Tests if a response is generated successfully with a valid API key."""
        # Mock the Gemini API's chat and send_message methods
        mock_response = unittest.mock.Mock()
        mock_response.text = "Hello there!"
        
        mock_chat_session = unittest.mock.Mock()
        mock_chat_session.send_message.return_value = mock_response
        
        mock_generative_model.return_value.start_chat.return_value = mock_chat_session
        
        processor = LLMProcessorGemini(self.config_manager, self.api_key_manager)
        result = processor.generate_response("Hi there.")
        
        mock_chat_session.send_message.assert_called_once_with("Hi there.")
        return result == "Hello there!"

    @unittest.mock.patch.object(APIKeyManager, 'get_key', return_value=None)
    def test_generate_response_without_key(self, mock_get_key) -> bool:
        """Tests if the service handles a missing API key gracefully."""
        processor = LLMProcessorGemini(self.config_manager, self.api_key_manager)
        result = processor.generate_response("Hi there.")
        
        return "not configured" in result

    def run_all_tests(self):
        """Runs all Gemini LLM processor tests."""
        self.test_runner.run_test("Successful Response Generation", self.test_generate_response_success)
        self.test_runner.run_test("Missing API Key Test", self.test_generate_response_without_key)
        self.test_runner.print_summary()
