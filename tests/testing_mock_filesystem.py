# File location: vidya/tests/testing_mock_filesystem.py

import logging
import tempfile
import os
import shutil

class MockFilesystem:
    """
    A context manager for creating and managing a temporary filesystem for tests.
    """
    def __init__(self):
        self.temp_dir = None
        self.original_cwd = os.getcwd()
        logging.info("MockFilesystem initialized.")

    def __enter__(self):
        """Creates a temporary directory and changes the current working directory to it."""
        self.temp_dir = tempfile.mkdtemp()
        os.chdir(self.temp_dir)
        logging.info(f"Mock filesystem created at '{self.temp_dir}'.")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleans up the temporary directory and restores the original working directory."""
        os.chdir(self.original_cwd)
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
        logging.info("Mock filesystem cleaned up.")
    
    def create_file(self, filename: str, content: str = ""):
        """Creates a file with the given content in the temporary directory."""
        with open(filename, 'w') as f:
            f.write(content)
        logging.info(f"File '{filename}' created in mock filesystem.")
        
    def create_dir(self, dirname: str):
        """Creates a directory in the temporary filesystem."""
        os.makedirs(dirname, exist_ok=True)
        logging.info(f"Directory '{dirname}' created in mock filesystem.")

    def get_path(self, filename: str) -> str:
        """Returns the full path to a file in the mock filesystem."""
        return os.path.join(self.temp_dir, filename)
