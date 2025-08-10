# File location: vidya/tests/testing_text_to_speech_huggingface.py

import logging
import unittest.mock
import os
from vidya.tests.testing_framework import TestingFramework
from vidya.audio.text_to_speech_huggingface import TextToSpeechHuggingFace

class TestingTextToSpeechHuggingFace:
    """
    A suite of tests to verify the functionality of the TextToSpeechHuggingFace.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        logging.info("TestingTextToSpeechHuggingFace initialized.")
    
    @unittest.mock.patch('transformers.pipeline')
    @unittest.mock.patch('soundfile.write')
    def test_successful_synthesis(self, mock_sf_write, mock_pipeline) -> bool:
        """Tests if text is successfully synthesized and saved."""
        # Mock the pipeline's return value to simulate audio data
        mock_pipeline.return_value = unittest.mock.Mock(
            return_value={'audio': [0.1, 0.2, 0.3], 'sampling_rate': 16000}
        )
        
        service = TextToSpeechHuggingFace()
        file_path = "test_output.wav"
        result = service.synthesize_speech("Hello, world!", file_path)
        
        # Verify that the mock methods were called correctly
        mock_pipeline.assert_called_once_with("Hello, world!")
        mock_sf_write.assert_called_once_with(file_path, [0.1, 0.2, 0.3], 16000)
        
        # Clean up the test file if it was created
        if os.path.exists(file_path):
            os.remove(file_path)
            
        return result == file_path

    @unittest.mock.patch('transformers.pipeline', side_effect=Exception("Model loading failed"))
    def test_loading_failure(self, mock_pipeline) -> bool:
        """Tests if the service handles model loading failure gracefully."""
        service = TextToSpeechHuggingFace()
        file_path = "test_output_fail.wav"
        result = service.synthesize_speech("Hello, world!", file_path)
        
        return result is None

    def run_all_tests(self):
        """Runs all Hugging Face TTS tests."""
        self.test_runner.run_test("Successful Synthesis Test", self.test_successful_synthesis)
        self.test_runner.run_test("Model Loading Failure Test", self.test_loading_failure)
        self.test_runner.print_summary()
