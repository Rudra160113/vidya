# File location: vidya/tests/testing_community_files.py

import logging
import os
from vidya.tests.testing_framework import TestingFramework

class TestingCommunityFiles:
    """
    A suite of tests to verify the presence of key community and documentation files.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.root_dir = os.path.join(os.path.dirname(__file__), '../../')
        self.required_files = [
            'README.md',
            'LICENSE.txt',
            'CONTRIBUTING.md',
            'CODE_OF_CONDUCT.md',
            '.github/ISSUE_TEMPLATE.md',
            '.github/PULL_REQUEST_TEMPLATE.md'
        ]
        logging.info("TestingCommunityFiles initialized.")

    def test_all_files_exist(self) -> bool:
        """Tests if all required community files are present in the repository."""
        missing_files = []
        for filename in self.required_files:
            file_path = os.path.join(self.root_dir, filename)
            if not os.path.exists(file_path):
                missing_files.append(filename)
                
        if missing_files:
            logging.error(f"The following required files are missing: {', '.join(missing_files)}")
            return False
        
        return True

    def run_all_tests(self):
        """Runs all community file presence tests."""
        self.test_runner.run_test("Required Community Files Test", self.test_all_files_exist)
        self.test_runner.print_summary()
