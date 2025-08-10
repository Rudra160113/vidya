# File location: vidya/features/app_access.py

import subprocess
import os
import logging
import platform

class AppAccess:
    """
    Provides methods to interact with and manage other applications on the system.
    """
    def __init__(self):
        self.os_type = platform.system()
        logging.info("AppAccess initialized.")

    def open_application(self, app_name: str) -> str:
        """
        Opens a specific application. This is a more robust version of the one
        in task_automation.py, designed to work across different OS types.
        """
        try:
            if self.os_type == "Windows":
                subprocess.Popen(app_name, shell=True)
            elif self.os_type == "Darwin": # macOS
                subprocess.Popen(["open", "-a", app_name])
            elif self.os_type == "Linux":
                subprocess.Popen([app_name])
            else:
                return "Unsupported operating system."
            
            logging.info(f"Successfully started application: {app_name}")
            return f"Okay, opening {app_name}."
        except FileNotFoundError:
            logging.error(f"Application not found: {app_name}")
            return f"Sorry, I couldn't find the application '{app_name}'."
        except Exception as e:
            logging.error(f"An error occurred while trying to open {app_name}: {e}")
            return f"An error occurred while trying to open '{app_name}'."

    def is_app_running(self, app_name: str) -> bool:
        """
        Checks if a specific application is currently running.
        This functionality can be complex and platform-dependent.
        """
        try:
            if self.os_type == "Windows":
                # Using tasklist to check for the process
                process = subprocess.Popen(['tasklist'], stdout=subprocess.PIPE, text=True)
                output, _ = process.communicate()
                return app_name.lower() in output.lower()
            elif self.os_type == "Darwin" or self.os_type == "Linux":
                # Using pgrep to check for the process
                process = subprocess.Popen(['pgrep', '-f', app_name], stdout=subprocess.PIPE, text=True)
                output, _ = process.communicate()
                return bool(output.strip())
            return False
        except Exception as e:
            logging.error(f"Failed to check if app '{app_name}' is running: {e}")
            return False
