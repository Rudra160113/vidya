# File location: vidya/tests/testing_scheduler_service.py

import logging
import asyncio
import time
from vidya.tests.testing_framework import TestingFramework
from vidya.core.scheduler_service import SchedulerService

class TestingSchedulerService:
    """
    A suite of tests to verify the functionality of the SchedulerService.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.scheduler = SchedulerService()
        logging.info("TestingSchedulerService initialized.")
        
    async def _mock_task(self, counter: list):
        """A mock task that increments a counter."""
        counter[0] += 1
        
    async def test_scheduled_task_runs_on_time(self) -> bool:
        """Tests if a scheduled task runs at the correct interval."""
        counter = [0]
        
        # Schedule the task to run every 1 second
        self.scheduler.schedule_task("test_task", self._mock_task(counter), interval=1)
        
        # Start the scheduler and let it run for a bit
        asyncio.create_task(self.scheduler.start())
        
        # Wait for 3.5 seconds, the task should have run 3 times
        await asyncio.sleep(3.5)
        
        self.scheduler.stop()
        
        # The counter should be at least 3
        return counter[0] >= 3

    def run_all_tests(self):
        """Runs all scheduler service tests."""
        asyncio.run(self.test_runner.run_async_test("Scheduled Task Interval Test", self.test_scheduled_task_runs_on_time))
        self.test_runner.print_summary()
