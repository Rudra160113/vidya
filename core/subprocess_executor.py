# File location: vidya/core/subprocess_executor.py

import logging
import subprocess
from vidya.utils.data_sanitizer import DataSanitizer

class SubprocessExecutor:
    """
    Executes system commands or scripts securely in a subprocess.
    """
    def __init__(self, data_sanitizer: DataSanitizer):
        self.data_sanitizer = data_sanitizer
        logging.info("SubprocessExecutor initialized.")
        
    def execute_command(self, command: str, timeout: int = 10) -> tuple:
        """
        Executes a shell command and returns the output and error.
        A very basic sanitization is applied.
        """
        # A simple, but not foolproof, sanitization step.
        sanitized_command = self.data_sanitizer.sanitize_shell_command(command)
        
        logging.info(f"Executing command: '{sanitized_command}'")
        
        try:
            # shell=True is for convenience but can be a security risk.
            # A more robust implementation would avoid it and pass a list of args.
            result = subprocess.run(
                sanitized_command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout,
                check=True
            )
            return (result.stdout, result.stderr)
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed with exit code {e.returncode}: {e.stderr}")
            return (e.stdout, e.stderr)
        except subprocess.TimeoutExpired as e:
            logging.warning(f"Command timed out after {timeout} seconds.")
            return ("", "Command timed out.")
        except Exception as e:
            logging.error(f"An error occurred while executing command: {e}")
            return ("", "An unexpected error occurred.")
