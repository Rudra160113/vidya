# File location: vidya/tests/testing_ci_hooks.py

import logging
import os
import shutil
from vidya.tests.testing_framework import TestingFramework
from vidya.ci.pre_commit_hooks import check_for_print_statements
from vidya.utils.style_checker import StyleChecker

class TestingCIHooks:
    """
    A suite of tests to verify the functionality of CI/CD-related scripts.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.temp_dir = "test_ci_dir"
        logging.info("TestingCIHooks initialized.")

    def _setup_test_environment(self):
        """Creates a temporary directory with test files."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        os.makedirs(self.temp_dir)
        
    def _cleanup_test_environment(self):
        """Removes the temporary directory."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_print_statement_detection(self) -> bool:
        """Tests if the pre-commit hook can find a print() statement."""
        self._setup_test_environment()
        
        # Create a file with a print statement
        bad_file_path = os.path.join(self.temp_dir, "bad_code.py")
        with open(bad_file_path, 'w') as f:
            f.write("print('Hello, world!')")
            
        result = check_for_print_statements([bad_file_path])
        self._cleanup_test_environment()
        return not result # The check should fail

    def test_style_checker_line_length(self) -> bool:
        """Tests if the style checker detects a line that is too long."""
        self._setup_test_environment()
        
        # Create a file with a very long line
        long_line_file_path = os.path.join(self.temp_dir, "long_line.py")
        with open(long_line_file_path, 'w') as f:
            f.write("x = 'a' * 150")
            
        checker = StyleChecker(root_dir=self.temp_dir)
        result = checker.run_checks()
        self._cleanup_test_environment()
        
        return "Line too long" in result

    def run_all_tests(self):
        """Runs all CI/CD-related tests."""
        self.test_runner.run_test("Print Statement Detection Test", self.test_print_statement_detection)
        self.test_runner.run_test("Style Checker Line Length Test", self.test_style_checker_line_length)
        self.test_runner.print_summary()
