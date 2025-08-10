# File location: vidya/core/task_runner.py

import logging
import time
from vidya.core.scheduler_service import SchedulerService
from vidya.core.task_executor import TaskExecutor
import threading

class TaskRunner:
    """
    A daemon that runs scheduled tasks.
    """
    def __init__(self, scheduler_service: SchedulerService, task_executor: TaskExecutor, polling_interval: int = 60):
        self.scheduler_service = scheduler_service
        self.task_executor = task_executor
        self.polling_interval = polling_interval
        self._running = False
        self._thread = None
        logging.info("TaskRunner initialized.")

    def start_runner(self):
        """Starts the task runner in a separate thread."""
        if self._running:
            return
        
        self._running = True
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()
        logging.info("Task runner started.")

    def stop_runner(self):
        """Stops the task runner."""
        self._running = False
        if self._thread:
            self._thread.join()
        logging.info("Task runner stopped.")

    def _run_loop(self):
        """The main loop for checking and executing scheduled tasks."""
        while self._running:
            try:
                self._execute_pending_tasks()
                time.sleep(self.polling_interval)
            except Exception as e:
                logging.error(f"Error in task runner loop: {e}")
                time.sleep(self.polling_interval)

    def _execute_pending_tasks(self):
        """Retrieves and executes all tasks that are due."""
        pending_tasks = self.scheduler_service.get_pending_tasks()
        
        for task in pending_tasks:
            task_id = task.get("id")
            task_type = task.get("task_type")
            task_data = task.get("task_data")
            
            logging.info(f"Executing scheduled task {task_id}: type='{task_type}'")
            
            # The TaskExecutor would need a new method to handle scheduled tasks
            # self.task_executor.execute_scheduled_task(task_type, task_data)
            
            # For now, we'll just log and mark as complete
            logging.warning(f"TaskExecutor placeholder: Would execute task '{task_type}' with data: {task_data}")
            
            # Mark the task as completed
            self._mark_task_as_complete(task_id)
            
    def _mark_task_as_complete(self, task_id: int):
        """Marks a task as completed in the database."""
        query = "UPDATE scheduled_tasks SET is_completed = 1 WHERE id = ?"
        self.scheduler_service.db_connector.execute_query(query, (task_id,))
        logging.info(f"Scheduled task {task_id} marked as completed.")
