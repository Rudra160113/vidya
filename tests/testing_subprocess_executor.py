# File location: vidya/tests/testing_subprocess_executor.py

import logging
import time
from vidya.tests.testing_framework import TestingFramework
from vidya.utils.subprocess_executor import SubprocessExecutor

class TestingSubprocessExecutor:
    """
    A suite of tests to verify the functionality of the SubprocessExecutor.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.executor = SubprocessExecutor()
        logging.info("TestingSubprocessExecutor initialized.")

    def test_valid_command(self) -> bool:
        """Tests if a valid command can be executed successfully."""
        result = self.executor.execute_command(["echo", "Hello, World!"])
        
        return result.strip() == "Hello, World!"

    def test_invalid_command(self) -> bool:
        """Tests if an invalid command returns an error."""
        result = self.executor.execute_command(["this_command_does_not_exist"])
        
        return "Command not found" in result

    def test_command_timeout(self) -> bool:
        """Tests if a long-running command is terminated by the timeout."""
        start_time = time.time()
        # Sleep for 5 seconds, but set a timeout of 1 second
        result = self.executor.execute_command(["sleep", "5"], timeout=1)
        end_time = time.time()
        
        # The result should indicate a timeout
        timeout_occurred = "Timeout" in result
        
        # The execution time should be less than the command's sleep time
        execution_time_is_short = (end_time - start_time) < 2
        
        return timeout_occurred and execution_time_is_short

    def run_all_tests(self):
        """Runs all subprocess executor tests."""
        self.test_runner.run_test("Valid Command Test", self.test_valid_command)
        self.test_runner.run_test("Invalid Command Test", self.test_invalid_command)
        self.test_runner.run_test("Command Timeout Test", self.test_command_timeout)
        self.test_runner.print_summary()
