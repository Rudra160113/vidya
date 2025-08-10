# File location: vidya/tests/testing_command_parser.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.nlp.command_parser import CommandParser

class TestingCommandParser:
    """
    A suite of tests to verify the functionality of the CommandParser.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.parser = CommandParser()
        logging.info("TestingCommandParser initialized.")

    def test_basic_command_parsing(self) -> bool:
        """Tests if a simple command is parsed correctly."""
        nlp_output = {
            'text': 'what is the weather in London',
            'entities': {
                'command': 'get_weather',
                'location': 'London'
            }
        }
        expected_command = {'name': 'get_weather', 'args': {'location': 'London'}}
        
        parsed_command = self.parser.parse_nlp_output(nlp_output)
        
        return parsed_command == expected_command

    def test_command_with_multiple_entities(self) -> bool:
        """Tests if a command with multiple arguments is parsed correctly."""
        nlp_output = {
            'text': 'set a reminder for 5 PM to call mom',
            'entities': {
                'command': 'set_reminder',
                'time': '5 PM',
                'task': 'call mom'
            }
        }
        expected_command = {'name': 'set_reminder', 'args': {'time': '5 PM', 'task': 'call mom'}}
        
        parsed_command = self.parser.parse_nlp_output(nlp_output)
        
        return parsed_command == expected_command

    def test_unknown_command(self) -> bool:
        """Tests if the parser returns a default 'unknown' command for unrecognized input."""
        nlp_output = {
            'text': 'this is a completely random sentence',
            'entities': {
                'command': 'unknown'
            }
        }
        expected_command = {'name': 'unknown', 'args': {}}
        
        parsed_command = self.parser.parse_nlp_output(nlp_output)
        
        return parsed_command == expected_command

    def run_all_tests(self):
        """Runs all command parser tests."""
        self.test_runner.run_test("Basic Command Parsing Test", self.test_basic_command_parsing)
        self.test_runner.run_test("Multiple Entities Test", self.test_command_with_multiple_entities)
        self.test_runner.run_test("Unknown Command Test", self.test_unknown_command)
        self.test_runner.print_summary()
