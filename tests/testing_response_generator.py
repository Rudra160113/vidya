# File location: vidya/tests/testing_response_generator.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.llm.response_generator import ResponseGenerator

class TestingResponseGenerator:
    """
    A suite of tests to verify the functionality of the ResponseGenerator.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.generator = ResponseGenerator()
        logging.info("TestingResponseGenerator initialized.")

    def test_simple_text_response(self) -> bool:
        """Tests if simple text is formatted correctly."""
        command_result = "Hello, I am Vidya."
        response = self.generator.generate(command_result)
        
        return response == "Hello, I am Vidya."

    def test_list_response(self) -> bool:
        """Tests if a list of items is formatted correctly."""
        command_result = ["Milk", "Bread", "Eggs"]
        response = self.generator.generate(command_result)
        
        expected_response = "Here are your items:\n- Milk\n- Bread\n- Eggs"
        return response == expected_response

    def test_error_response(self) -> bool:
        """Tests if an error message is formatted correctly."""
        command_result = {"status": "error", "message": "Command failed to execute."}
        response = self.generator.generate(command_result)
        
        expected_response = "I'm sorry, I encountered an error: Command failed to execute."
        return response == expected_response
        
    def test_unrecognized_response(self) -> bool:
        """Tests how the generator handles an unrecognized response format."""
        command_result = 12345
        response = self.generator.generate(command_result)
        
        expected_response = "I'm sorry, I couldn't understand that result."
        return response == expected_response

    def run_all_tests(self):
        """Runs all response generator tests."""
        self.test_runner.run_test("Simple Text Response Test", self.test_simple_text_response)
        self.test_runner.run_test("List Response Test", self.test_list_response)
        self.test_runner.run_test("Error Response Test", self.test_error_response)
        self.test_runner.run_test("Unrecognized Response Test", self.test_unrecognized_response)
        self.test_runner.print_summary()
