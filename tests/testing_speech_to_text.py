# File location: vidya/tests/testing_speech_to_text.py

import logging
import os
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.services.speech_to_text_service import SpeechToTextService
from vidya.security.api_key_manager import APIKeyManager
from vidya.config.configuration_manager import ConfigurationManager
import openai

class TestingSpeechToText:
    """
    A suite of tests to verify the functionality of the SpeechToTextService.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.config_manager = ConfigurationManager()
        self.api_key_manager = APIKeyManager(unittest.mock.MagicMock(), self.config_manager)
        
        logging.info("TestingSpeechToText initialized.")

    @unittest.mock.patch('openai.Audio.transcribe')
    @unittest.mock.patch.object(APIKeyManager, 'get_key', return_value='mock-api-key')
    def test_transcribe_success(self, mock_get_key, mock_transcribe) -> bool:
        """Tests if an audio file can be transcribed successfully."""
        mock_transcribe.return_value = {'text': 'Hello, world.'}
        
        service = SpeechToTextService(self.config_manager, self.api_key_manager)
        
        # Create a dummy audio file for the test
        dummy_audio_file = "dummy_audio.wav"
        with open(dummy_audio_file, 'w') as f:
            f.write("dummy data")
            
        result = service.transcribe_audio(dummy_audio_file)
        os.remove(dummy_audio_file)
        
        mock_transcribe.assert_called_once()
        return result == "Hello, world."

    @unittest.mock.patch('openai.Audio.transcribe')
    @unittest.mock.patch.object(APIKeyManager, 'get_key', return_value=None)
    def test_transcribe_without_key(self, mock_get_key, mock_transcribe) -> bool:
        """Tests if the service handles a missing API key gracefully."""
        service = SpeechToTextService(self.config_manager, self.api_key_manager)
        
        dummy_audio_file = "dummy_audio.wav"
        with open(dummy_audio_file, 'w') as f:
            f.write("dummy data")
            
        result = service.transcribe_audio(dummy_audio_file)
        os.remove(dummy_audio_file)
        
        mock_transcribe.assert_not_called()
        return result is None

    def run_all_tests(self):
        """Runs all speech-to-text tests."""
        self.test_runner.run_test("Successful Transcription Test", self.test_transcribe_success)
        self.test_runner.run_test("Missing API Key Test", self.test_transcribe_without_key)
        self.test_runner.print_summary()
