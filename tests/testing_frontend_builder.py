# File location: vidya/tests/testing_frontend_builder.py

import logging
import os
import shutil
from vidya.tests.testing_framework import TestingFramework
from vidya.client.frontend_builder import FrontendBuilder

class TestingFrontendBuilder:
    """
    A suite of tests to verify the functionality of the FrontendBuilder.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.temp_dir = "test_frontend_dir"
        logging.info("TestingFrontendBuilder initialized.")

    def _setup_test_environment(self):
        """Creates a temporary frontend directory."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)

    def _cleanup_test_environment(self):
        """Removes the temporary directory."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_successful_build(self) -> bool:
        """Tests if a build can be successfully initiated."""
        self._setup_test_environment()
        
        builder = FrontendBuilder(frontend_dir=self.temp_dir)
        result = builder.build()
        
        self._cleanup_test_environment()
        
        return "successful" in result.lower()

    def test_build_with_missing_directory(self) -> bool:
        """Tests if the builder handles a missing frontend directory gracefully."""
        self._cleanup_test_environment()
        
        builder = FrontendBuilder(frontend_dir="nonexistent_dir")
        result = builder.build()
        
        return "not found" in result.lower()

    def run_all_tests(self):
        """Runs all frontend builder tests."""
        self.test_runner.run_test("Successful Build Test", self.test_successful_build)
        self.test_runner.run_test("Missing Directory Test", self.test_build_with_missing_directory)
        self.test_runner.print_summary()
