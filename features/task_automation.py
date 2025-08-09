# File location: vidya/features/task_automation.py

import os
import subprocess
import logging

class TaskAutomation:
    """
    Automates tasks like opening applications, files, or running scripts.
    """
    def __init__(self):
        logging.info("TaskAutomation initialized.")

    def open_application(self, app_name: str) -> str:
        """
        Opens a specified application on the user's system.
        This function's behavior is platform-dependent.
        """
        app_name = app_name.lower()
        try:
            if os.name == 'nt':  # For Windows
                subprocess.Popen(app_name, shell=True)
            elif os.name == 'posix':  # For Linux and macOS
                subprocess.Popen(['open', app_name])
            else:
                return f"Unsupported operating system: {os.name}"

            logging.info(f"Successfully started application: {app_name}")
            return f"Opening {app_name}."
        except FileNotFoundError:
            logging.error(f"Application not found: {app_name}")
            return f"Sorry, I couldn't find the application: {app_name}."
        except Exception as e:
            logging.error(f"An error occurred while trying to open {app_name}: {e}")
            return f"An error occurred while trying to open {app_name}."

    def open_file(self, file_path: str) -> str:
        """
        Opens a specified file. The default program for that file type will be used.
        """
        try:
            if os.path.exists(file_path):
                os.startfile(file_path) if os.name == 'nt' else subprocess.Popen(['open', file_path])
                logging.info(f"Successfully opened file: {file_path}")
                return f"Opening {os.path.basename(file_path)}."
            else:
                logging.error(f"File not found: {file_path}")
                return f"Sorry, the file at '{file_path}' was not found."
        except Exception as e:
            logging.error(f"An error occurred while trying to open file {file_path}: {e}")
            return f"An error occurred while trying to open the file."
