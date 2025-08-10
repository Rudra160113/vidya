# File location: vidya/tests/testing_task_runner.py

import logging
import time
from vidya.tests.testing_framework import TestingFramework
from vidya.core.task_runner import TaskRunner

class TestingTaskRunner:
    """
    A suite of tests to verify the functionality of the TaskRunner.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        logging.info("TestingTaskRunner initialized.")
    
    def _mock_target_function(self, value: int, delay: int) -> int:
        """A mock function to be run by the TaskRunner."""
        time.sleep(delay)
        return value * 2

    def test_task_execution_and_result(self) -> bool:
        """Tests if a task can be started and its result retrieved."""
        runner = TaskRunner(self._mock_target_function, value=10, delay=1)
        runner.start()
        
        # Check that the thread is alive
        thread_is_alive = runner.is_alive()
        
        # Wait for the task to complete
        runner.join(timeout=2)
        
        # The thread should no longer be alive
        thread_is_stopped = not runner.is_alive()
        
        # The result should be correct
        result = runner.get_result()
        
        return thread_is_alive and thread_is_stopped and result == 20

    def test_timeout_on_task(self) -> bool:
        """Tests if the join method correctly handles a timeout."""
        runner = TaskRunner(self._mock_target_function, value=10, delay=5)
        runner.start()
        
        # Wait for a shorter duration than the task's execution time
        runner.join(timeout=1)
        
        # The thread should still be alive
        thread_is_alive = runner.is_alive()
        
        # Clean up the running thread to prevent it from hanging
        runner.join()
        
        return thread_is_alive

    def run_all_tests(self):
        """Runs all task runner tests."""
        self.test_runner.run_test("Task Execution and Result Test", self.test_task_execution_and_result)
        self.test_runner.run_test("Timeout Test", self.test_timeout_on_task)
        self.test_runner.print_summary()
