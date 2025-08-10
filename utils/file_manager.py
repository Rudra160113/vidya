# File location: vidya/utils/file_manager.py

import logging
import os
import tempfile
from typing import Any

class FileManager:
    """
    A utility class for managing file-system operations.
    """
    def __init__(self):
        self.temp_dir = tempfile.gettempdir()
        logging.info("FileManager initialized.")

    def write_file(self, file_path: str, content: str | bytes) -> bool:
        """
        Writes content to a specified file.
        
        Args:
            file_path (str): The path to the file.
            content (str | bytes): The content to write.
            
        Returns:
            bool: True on success, False on failure.
        """
        try:
            mode = 'w' if isinstance(content, str) else 'wb'
            with open(file_path, mode) as f:
                f.write(content)
            logging.info(f"Successfully wrote content to file: {file_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to write to file '{file_path}': {e}")
            return False

    def read_file(self, file_path: str) -> str | bytes | None:
        """
        Reads content from a specified file.
        
        Args:
            file_path (str): The path to the file.
            
        Returns:
            str | bytes | None: The file content, or None on failure.
        """
        try:
            mode = 'r' if file_path.endswith('.txt') or file_path.endswith('.json') else 'rb'
            with open(file_path, mode) as f:
                content = f.read()
            return content
        except FileNotFoundError:
            logging.warning(f"File not found: {file_path}")
            return None
        except Exception as e:
            logging.error(f"Failed to read file '{file_path}': {e}")
            return None

    def create_temp_file(self, suffix: str = '') -> str:
        """
        Creates a temporary file and returns its path. The file is
        automatically removed when the context is exited.
        
        Args:
            suffix (str): The suffix for the temporary file.
            
        Returns:
            str: The path to the created temporary file.
        """
        # This is a simple implementation. A more robust one might use a
        # context manager.
        fd, path = tempfile.mkstemp(suffix=suffix, dir=self.temp_dir)
        os.close(fd)
        logging.info(f"Created temporary file: {path}")
        return path
