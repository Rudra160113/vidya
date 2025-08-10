# File location: vidya/core/code_executor.py

import logging
import io
import contextlib

class CodeExecutor:
    """
    Executes Python code safely within a controlled environment.
    
    WARNING: Executing arbitrary code from an external source is a
    significant security risk. This implementation is a simplified
    demonstration and lacks a secure sandboxing mechanism.
    A production-level system would use a dedicated, isolated
    environment (e.g., a container or a separate process with
    restricted permissions) to run this code.
    """
    def __init__(self):
        logging.warning("CodeExecutor is active. Ensure code is sanitized and executed in a secure sandbox.")
        self.local_vars = {} # For maintaining state across executions

    def execute_code(self, code_string: str) -> str:
        """
        Executes a string of Python code and captures the output.
        """
        # Capture stdout and stderr
        old_stdout = io.StringIO()
        old_stderr = io.StringIO()
        
        try:
            with contextlib.redirect_stdout(old_stdout), contextlib.redirect_stderr(old_stderr):
                exec(code_string, {}, self.local_vars)
            
            output = old_stdout.getvalue().strip()
            error_output = old_stderr.getvalue().strip()

            if error_output:
                logging.error(f"Error during code execution: {error_output}")
                return f"Error: {error_output}"
            
            logging.info("Code executed successfully.")
            return output if output else "Code executed with no output."
            
        except Exception as e:
            logging.error(f"An unexpected exception occurred during code execution: {e}")
            return f"An exception occurred: {e}"
