# File location: vidya/tests/testing_integration_subprocess.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.core.subprocess_executor import SubprocessExecutor
from vidya.utils.data_sanitizer import DataSanitizer

class TestingIntegrationSubprocess:
    """
    A suite of integration tests for the SubprocessExecutor.
    """
    def __init__(self):
        self.data_sanitizer = DataSanitizer()
        self.executor = SubprocessExecutor(self.data_sanitizer)
        self.test_runner = TestingFramework()
        logging.info("TestingIntegrationSubprocess initialized.")

    def test_basic_command_execution(self) -> bool:
        """Tests a simple command that should succeed."""
        command = "echo Hello World"
        stdout, stderr = self.executor.execute_command(command)
        return stdout.strip() == "Hello World" and not stderr

    def test_failing_command_execution(self) -> bool:
        """Tests a command that should fail and produce an error."""
        command = "this-command-does-not-exist"
        stdout, stderr = self.executor.execute_command(command)
        return not stdout and "not found" in stderr.lower()

    def test_command_injection_prevention(self) -> bool:
        """
        Tests if the data sanitizer prevents a command injection attack.
        Note: The sanitizer is a simple placeholder.
        """
        command = "echo bad; rm -rf /"
        stdout, stderr = self.executor.execute_command(command)
        # We check that the 'rm' command was not executed.
        return stdout.strip() == "bad" and not stderr

    def run_all_tests(self):
        """Runs all subprocess-related integration tests."""
        self.test_runner.run_test("Basic Command Test", self.test_basic_command_execution)
        self.test_runner.run_test("Failing Command Test", self.test_failing_command_execution)
        self.test_runner.run_test("Injection Prevention Test", self.test_command_injection_prevention)
        self.test_runner.print_summary()
