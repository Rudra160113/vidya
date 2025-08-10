# File location: vidya/features/file_handler.py

import os
import shutil
import logging

class FileHandler:
    """
    Handles file and directory operations on the local file system.
    """
    def __init__(self):
        logging.info("FileHandler initialized.")

    def create_directory(self, dir_path: str) -> str:
        """Creates a new directory if it does not already exist."""
        try:
            os.makedirs(dir_path, exist_ok=True)
            logging.info(f"Directory created or already exists: {dir_path}")
            return f"Directory '{os.path.basename(dir_path)}' created successfully."
        except OSError as e:
            logging.error(f"Failed to create directory {dir_path}: {e}")
            return f"An error occurred while creating the directory: {e}"

    def create_file(self, file_path: str, content: str = "") -> str:
        """Creates a new file with optional content."""
        try:
            with open(file_path, 'w') as f:
                f.write(content)
            logging.info(f"File created successfully: {file_path}")
            return f"File '{os.path.basename(file_path)}' created successfully."
        except IOError as e:
            logging.error(f"Failed to create file {file_path}: {e}")
            return f"An error occurred while creating the file: {e}"

    def delete_file(self, file_path: str) -> str:
        """Deletes a file."""
        try:
            if os.path.exists(file_path) and os.path.isfile(file_path):
                os.remove(file_path)
                logging.info(f"File deleted successfully: {file_path}")
                return f"File '{os.path.basename(file_path)}' deleted."
            else:
                logging.warning(f"File not found or is not a file: {file_path}")
                return "File not found or is not a file."
        except OSError as e:
            logging.error(f"Failed to delete file {file_path}: {e}")
            return f"An error occurred while deleting the file: {e}"
