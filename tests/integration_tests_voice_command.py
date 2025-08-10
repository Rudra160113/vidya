# File location: vidya/tests/integration_tests_voice_command.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.audio.speech_to_text_service import SpeechToTextService
from vidya.nlp.voice_command_parser import VoiceCommandParser
from vidya.nlp.nlp_processor import NLPProcessor
from vidya.core.command_executor import CommandExecutor
from vidya.core.command_router import CommandRouter
from vidya.core.dependency_injector import DependencyInjector

class IntegrationTestsVoiceCommand:
    """
    A suite of integration tests to verify the voice command pipeline.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup Dependency Injector and mock services
        self.injector = DependencyInjector()
        self.mock_stt_service = unittest.mock.Mock(spec=SpeechToTextService)
        self.mock_nlp_processor = unittest.mock.Mock(spec=NLPProcessor)
        self.router = CommandRouter()
        
        self.injector.register(SpeechToTextService, self.mock_stt_service)
        self.injector.register(NLPProcessor, self.mock_nlp_processor)
        self.injector.register(CommandRouter, self.router)
        
        self.parser = VoiceCommandParser(self.injector)
        self.executor = CommandExecutor(self.injector)
        
        logging.info("Voice Command Integration Test Suite initialized.")
    
    def test_voice_command_pipeline(self) -> bool:
        """
        Simulates the full end-to-end process of a voice command.
        """
        # Step 1: Mock the speech-to-text service
        self.mock_stt_service.transcribe_audio.return_value = "What is the weather in London?"
        
        # Step 2: Mock the NLP processor
        self.mock_nlp_processor.process.return_value = {
            "command": "get_weather",
            "entities": {"location": "London"}
        }
        
        # Step 3: Define and register a mock command handler
        mock_weather_handler = unittest.mock.Mock(return_value="The weather in London is sunny.")
        self.router.register_handler("get_weather", mock_weather_handler)
        
        # Step 4: Run the pipeline
        audio_file_path = "test_audio.wav"
        transcribed_text = self.mock_stt_service.transcribe_audio(audio_file_path)
        parsed_command = self.parser.parse(transcribed_text)
        result = self.executor.execute_command(parsed_command)
        
        # Step 5: Verify all steps were called and the result is correct
        self.mock_stt_service.transcribe_audio.assert_called_once_with(audio_file_path)
        self.mock_nlp_processor.process.assert_called_once_with("What is the weather in London?")
        mock_weather_handler.assert_called_once_with({"location": "London"})
        
        return result == "The weather in London is sunny."

    def run_all_tests(self):
        """Runs all voice command integration tests."""
        self.test_runner.run_test("Voice Command Pipeline Test", self.test_voice_command_pipeline)
        self.test_runner.print_summary()
