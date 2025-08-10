# File location: vidya/tests/testing_text_to_speech.py

import logging
import os
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.services.text_to_speech_service import TextToSpeechService
from vidya.config.configuration_manager import ConfigurationManager

class TestingTextToSpeech:
    """
    A suite of tests to verify the functionality of the TextToSpeechService.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.config_manager = ConfigurationManager()
        self.config_manager.config_data = {'tts_api_url': 'http://mock-tts-api.com/synthesize'}
        self.tts_service = TextToSpeechService(self.config_manager)
        self.output_file = "test_output.wav"
        
        logging.info("TestingTextToSpeech initialized.")

    def _cleanup(self):
        """Removes the test output file."""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    @unittest.mock.patch('requests.post')
    @unittest.mock.patch('pydub.AudioSegment.from_file')
    def test_synthesize_success(self, mock_from_file, mock_post) -> bool:
        """Tests if speech can be synthesized and saved to a file."""
        self._cleanup()
        
        # Mock the API response
        mock_response = unittest.mock.Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.content = b'mock audio data'
        mock_post.return_value = mock_response
        
        # Mock the AudioSegment object and its export method
        mock_audio_segment = unittest.mock.Mock()
        mock_from_file.return_value = mock_audio_segment
        
        result = self.tts_service.synthesize_speech("Hello, world.", self.output_file)
        
        self._cleanup()
        
        mock_post.assert_called_once()
        mock_from_file.assert_called_once()
        mock_audio_segment.export.assert_called_once_with(self.output_file, format="wav")
        
        return result

    @unittest.mock.patch('requests.post', side_effect=Exception("API error"))
    def test_synthesize_failure(self, mock_post) -> bool:
        """Tests if the service handles an API failure gracefully."""
        self._cleanup()
        
        result = self.tts_service.synthesize_speech("Hello, world.", self.output_file)
        
        self._cleanup()
        
        return not result

    def run_all_tests(self):
        """Runs all text-to-speech tests."""
        self.test_runner.run_test("Successful Speech Synthesis Test", self.test_synthesize_success)
        self.test_runner.run_test("Speech Synthesis Failure Test", self.test_synthesize_failure)
        self.test_runner.print_summary()
