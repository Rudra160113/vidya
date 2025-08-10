# File location: vidya/tests/testing_data_processor.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.utils.data_processor import DataProcessor

class TestingDataProcessor:
    """
    A suite of tests to verify the functionality of the DataProcessor.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.processor = DataProcessor()
        logging.info("TestingDataProcessor initialized.")
    
    def test_sanitize_string(self) -> bool:
        """Tests if the string sanitizer works correctly."""
        raw_string = "  Hello, World!   "
        sanitized = self.processor.sanitize_string(raw_string)
        
        return sanitized == "Hello, World!"

    def test_validate_dict_keys(self) -> bool:
        """Tests if dictionary key validation works as expected."""
        valid_data = {"key1": 1, "key2": 2}
        invalid_data = {"key1": 1}
        
        is_valid = self.processor.validate_dict_keys(valid_data, ["key1", "key2"])
        is_invalid = self.processor.validate_dict_keys(invalid_data, ["key1", "key2"])
        
        return is_valid and not is_invalid

    def test_get_safe_value(self) -> bool:
        """Tests safe retrieval of a value from a dictionary."""
        data = {"exists": "value"}
        
        existing_value = self.processor.get_safe_value(data, "exists")
        non_existing_value = self.processor.get_safe_value(data, "non_exists", default="default_val")
        
        return existing_value == "value" and non_existing_value == "default_val"

    def test_transform_to_snake_case(self) -> bool:
        """Tests if keys are correctly transformed to snake_case."""
        camel_case_data = {"camelCaseKey": "value", "anotherCamelCaseKey": "anotherValue"}
        snake_case_data = self.processor.transform_to_snake_case(camel_case_data)
        
        return "camel_case_key" in snake_case_data and "another_camel_case_key" in snake_case_data

    def run_all_tests(self):
        """Runs all data processor tests."""
        self.test_runner.run_test("Sanitize String Test", self.test_sanitize_string)
        self.test_runner.run_test("Validate Dict Keys Test", self.test_validate_dict_keys)
        self.test_runner.run_test("Get Safe Value Test", self.test_get_safe_value)
        self.test_runner.run_test("Transform to Snake Case Test", self.test_transform_to_snake_case)
        self.test_runner.print_summary()
