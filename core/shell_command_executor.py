# File location: vidya/core/shell_command_executor.py

import subprocess
import logging

class ShellCommandExecutor:
    """
    Executes shell commands on the local system.
    
    WARNING: Similar to the CodeExecutor, this module presents a
    significant security risk if not properly sanitized and
    restricted. Arbitrary shell commands can harm the system.
    """
    def __init__(self):
        logging.warning("ShellCommandExecutor is active. Be cautious about which commands are executed.")
        
    def execute_command(self, command: str) -> str:
        """
        Executes a shell command and returns its output.
        """
        try:
            # Using shell=True for simple commands is okay, but for production
            # it's safer to pass a list of arguments and set shell=False
            result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True, timeout=10)
            
            output = result.stdout.strip()
            error_output = result.stderr.strip()
            
            if error_output:
                logging.warning(f"Command '{command}' produced an error output: {error_output}")
                # We return the error output, as it might be a valid response
                return error_output
            
            logging.info(f"Command '{command}' executed successfully.")
            return output if output else "Command executed with no output."
            
        except subprocess.TimeoutExpired:
            logging.error(f"Command '{command}' timed out.")
            return "Command timed out."
        except subprocess.CalledProcessError as e:
            logging.error(f"Command '{command}' failed with exit code {e.returncode}: {e.stderr}")
            return f"Command failed: {e.stderr}"
        except Exception as e:
            logging.error(f"An unexpected exception occurred during command execution: {e}")
            return f"An exception occurred: {e}"
