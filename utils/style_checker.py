# File location: vidya/utils/style_checker.py

import logging
import os
import re

class StyleChecker:
    """
    Checks the codebase for custom style rules.
    This is a placeholder for a more complex tool like `Pylint` or `Flake8`.
    """
    def __init__(self, root_dir: str = 'vidya'):
        self.root_dir = root_dir
        self.errors = []
        logging.info("StyleChecker initialized.")

    def run_checks(self):
        """
        Recursively checks all Python files in the root directory.
        """
        logging.info("Running style checks...")
        for root, _, files in os.walk(self.root_dir):
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    self._check_file(file_path)
        
        if self.errors:
            logging.error(f"--- Style Checks Failed with {len(self.errors)} errors ---")
            for error in self.errors:
                logging.error(error)
            return "Style checks failed."
        else:
            logging.info("All style checks passed.")
            return "All style checks passed."

    def _check_file(self, file_path: str):
        """
        Checks a single file against a set of style rules.
        """
        with open(file_path, 'r') as f:
            for line_number, line in enumerate(f, 1):
                # Example rule 1: No more than 120 characters per line
                if len(line) > 120:
                    self.errors.append(f"Line too long in {file_path}:{line_number} ({len(line)} chars).")
                
                # Example rule 2: Use of double quotes for strings
                if re.search(r"'(.*?)'", line) and not re.search(r'"""|[\'"].*?[\'"]', line):
                    self.errors.append(f"Single quotes found in {file_path}:{line_number}. Use double quotes.")
