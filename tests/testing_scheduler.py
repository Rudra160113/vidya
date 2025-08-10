# File location: vidya/tests/testing_scheduler.py

import logging
from datetime import datetime, timedelta
import time
from vidya.tests.testing_framework import TestingFramework
from vidya.data.database_connector import DatabaseConnector
from vidya.core.scheduler_service import SchedulerService
from vidya.core.task_runner import TaskRunner
from vidya.core.task_executor import TaskExecutor
import threading

class TestingScheduler:
    """
    A suite of tests to verify the task scheduling and execution system.
    """
    def __init__(self):
        self.db_connector = DatabaseConnector(db_path=':memory:')
        self.db_connector.setup_database()
        self.scheduler_service = SchedulerService(self.db_connector)
        
        # Mock the task executor to just log the task
        self.mock_task_executor = TaskExecutor()
        self.mock_task_executor._run_scheduled_task = self._mock_task_action
        self.task_runner = TaskRunner(self.scheduler_service, self.mock_task_executor, polling_interval=1)
        
        self.test_runner = TestingFramework()
        self.executed_tasks = []
        logging.info("TestingScheduler initialized with in-memory DB.")

    def _mock_task_action(self, task_type: str, task_data: dict):
        """A mock action to be performed by the task runner."""
        self.executed_tasks.append((task_type, task_data))
        logging.info(f"Mock task '{task_type}' executed with data {task_data}.")

    def test_scheduled_task_execution(self) -> bool:
        """Tests if a task scheduled for the near future is executed."""
        self.executed_tasks = []
        
        # Schedule a task to run in 2 seconds
        future_time = datetime.now() + timedelta(seconds=2)
        task_data = {"message": "Hello from scheduled task."}
        self.scheduler_service.schedule_task("test_task", task_data, future_time)
        
        self.task_runner.start_runner()
        
        # Wait for a few seconds to let the task runner do its job
        time.sleep(4)
        
        self.task_runner.stop_runner()
        
        # Check if the task was executed
        if len(self.executed_tasks) != 1:
            return False
            
        executed_task_type, executed_task_data = self.executed_tasks[0]
        return executed_task_type == "test_task" and executed_task_data == task_data

    def run_all_tests(self):
        """Runs all scheduler-related integration tests."""
        self.test_runner.run_test("Scheduled Task Execution Test", self.test_scheduled_task_execution)
        self.test_runner.print_summary()
