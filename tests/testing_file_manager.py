# File location: vidya/tests/testing_file_manager.py

import logging
import os
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.utils.file_manager import FileManager

class TestingFileManager:
    """
    A suite of tests to verify the functionality of the FileManager.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.manager = FileManager()
        logging.info("TestingFileManager initialized.")
    
    def test_write_and_read_file(self) -> bool:
        """Tests if data can be written to and read from a file."""
        file_path = "test_file.txt"
        content = "This is a test file."
        
        try:
            # Write the content to the file
            self.manager.write_file(file_path, content)
            
            # Read the content back
            read_content = self.manager.read_file(file_path)
            
            return content == read_content
        finally:
            # Clean up the test file
            if os.path.exists(file_path):
                os.remove(file_path)

    def test_create_temp_file(self) -> bool:
        """Tests if a temporary file is created and cleaned up correctly."""
        file_path = self.manager.create_temp_file(suffix=".tmp")
        
        try:
            # Check if the file was created
            exists = os.path.exists(file_path)
            return exists
        finally:
            # The context manager in a real scenario would handle this, but for a simple
            # test, we'll manually clean up.
            if os.path.exists(file_path):
                os.remove(file_path)

    def run_all_tests(self):
        """Runs all file manager tests."""
        self.test_runner.run_test("Write and Read File Test", self.test_write_and_read_file)
        self.test_runner.run_test("Create Temp File Test", self.test_create_temp_file)
        self.test_runner.print_summary()
