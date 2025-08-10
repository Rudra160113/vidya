# File location: vidya/tests/testing_voice_command_parser.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.nlp.voice_command_parser import VoiceCommandParser
from vidya.nlp.nlp_processor import NLPProcessor
from vidya.core.dependency_injector import DependencyInjector

class TestingVoiceCommandParser:
    """
    A suite of tests to verify the functionality of the VoiceCommandParser.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup Dependency Injector with a mock NLPProcessor
        self.injector = DependencyInjector()
        self.mock_nlp_processor = unittest.mock.Mock(spec=NLPProcessor)
        self.injector.register(NLPProcessor, self.mock_nlp_processor)
        
        self.parser = VoiceCommandParser(self.injector)
        logging.info("TestingVoiceCommandParser initialized.")

    def test_successful_parsing(self) -> bool:
        """Tests if a valid command is parsed correctly."""
        self.mock_nlp_processor.process.return_value = {
            "command": "play_music",
            "entities": {"artist": "The Beatles"}
        }
        
        command = self.parser.parse("play some music by The Beatles")
        
        self.mock_nlp_processor.process.assert_called_once_with("play some music by The Beatles")
        
        return command['name'] == 'play_music' and command['args']['artist'] == 'The Beatles'

    def test_unrecognized_command(self) -> bool:
        """Tests if an unrecognized command is handled correctly."""
        self.mock_nlp_processor.process.return_value = {
            "command": "unrecognized",
            "entities": {}
        }
        
        command = self.parser.parse("this is some random text")
        
        self.mock_nlp_processor.process.assert_called_once_with("this is some random text")
        
        return command['name'] == 'unrecognized'

    def test_empty_input(self) -> bool:
        """Tests how the parser handles empty or null input."""
        command = self.parser.parse("")
        
        # The NLP processor should not be called for empty input
        self.mock_nlp_processor.process.assert_not_called()
        
        return command['name'] == 'unrecognized' and command['args']['reason'] == 'empty_input'

    def run_all_tests(self):
        """Runs all voice command parser tests."""
        self.test_runner.run_test("Successful Parsing Test", self.test_successful_parsing)
        self.test_runner.run_test("Unrecognized Command Test", self.test_unrecognized_command)
        self.test_runner.run_test("Empty Input Test", self.test_empty_input)
        self.test_runner.print_summary()
