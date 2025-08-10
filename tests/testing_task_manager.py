# File location: vidya/tests/testing_task_manager.py

import logging
import asyncio
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.core.task_manager import TaskManager
from vidya.core.dependency_injector import DependencyInjector

class TestingTaskManager:
    """
    A suite of tests to verify the functionality of the TaskManager.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.injector = DependencyInjector()
        self.manager = TaskManager(self.injector)
        logging.info("TestingTaskManager initialized.")

    async def _mock_coroutine(self, delay: int):
        """A mock coroutine that simulates a long-running task."""
        await asyncio.sleep(delay)
        return "Task completed"

    async def test_start_and_track_task(self) -> bool:
        """Tests if a task can be started and its status is tracked correctly."""
        task_id = "test_task_1"
        await self.manager.start_task(task_id, self._mock_coroutine, 1)
        
        # Immediately after starting, the task should be running
        status = self.manager.get_task_status(task_id)
        
        # Wait for the task to complete
        await asyncio.sleep(1.1)
        
        # After completion, the task status should be "Done"
        final_status = self.manager.get_task_status(task_id)
        
        return status == "Running" and final_status == "Done"

    async def test_cancel_task(self) -> bool:
        """Tests if a running task can be successfully canceled."""
        task_id = "test_task_2"
        await self.manager.start_task(task_id, self._mock_coroutine, 5)
        
        # Cancel the task before it can complete
        success = self.manager.cancel_task(task_id)
        
        # Check if the task is no longer in the active_tasks dictionary
        task_is_gone = task_id not in self.manager.active_tasks
        
        return success and task_is_gone

    async def run_all_tests(self):
        """Runs all task manager tests."""
        await self.test_runner.run_async_test("Start and Track Task Test", self.test_start_and_track_task)
        await self.test_runner.run_async_test("Cancel Task Test", self.test_cancel_task)
        self.test_runner.print_summary()
