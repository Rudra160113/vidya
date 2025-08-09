# File location: vidya/utils/permission_handler.py

import os
import logging
import sys

class PermissionHandler:
    """
    Handles requesting and checking necessary system permissions.
    """
    def __init__(self):
        logging.info("PermissionHandler initialized.")

    def request_all_permissions(self):
        """
        A centralized method to check for and request all needed permissions.
        """
        logging.info("Requesting all necessary permissions...")
        self.check_file_access()
        # Add more permission checks as needed (e.g., microphone access, network access)
        logging.info("All permissions checked.")

    def check_file_access(self, path: str = '.'):
        """
        Checks if the application has read/write access to a specific directory.
        """
        try:
            if not os.access(path, os.R_OK):
                logging.warning(f"Read access denied for directory: {path}")
                # On some systems, this might require a manual prompt
                self._prompt_for_permission(path, "read")
            
            if not os.access(path, os.W_OK):
                logging.warning(f"Write access denied for directory: {path}")
                self._prompt_for_permission(path, "write")

        except Exception as e:
            logging.error(f"Error checking file access: {e}")

    def _prompt_for_permission(self, path: str, permission_type: str):
        """
        Helper method to inform the user about a denied permission.
        """
        if sys.platform == "darwin" or sys.platform == "linux":
            print(f"Warning: Vidya requires {permission_type} access to '{path}'. "
                  f"Please grant this permission manually in your system settings.")
        elif sys.platform == "win32":
            print(f"Warning: Vidya requires {permission_type} access to '{path}'. "
                  f"Please run the application as an administrator or grant the necessary permissions.")
