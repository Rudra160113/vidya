# File location: vidya/features/scheduler.py

import schedule
import time
import threading
import logging

class Scheduler:
    """
    A simple task scheduler to run tasks at specified times or intervals.
    """
    def __init__(self):
        self.scheduler_thread = threading.Thread(target=self._run_schedule, daemon=True)
        self.scheduler_thread.start()
        logging.info("Scheduler initialized and running in a background thread.")

    def _run_schedule(self):
        """Internal method to run the scheduler loop."""
        while True:
            schedule.run_pending()
            time.sleep(1)

    def schedule_task_at(self, task_func, task_time: str, *args, **kwargs) -> str:
        """
        Schedules a task to run once at a specific time (e.g., "10:30").
        """
        try:
            schedule.every().day.at(task_time).do(task_func, *args, **kwargs)
            logging.info(f"Task '{task_func.__name__}' scheduled for {task_time}.")
            return f"Task '{task_func.__name__}' scheduled to run at {task_time} today."
        except Exception as e:
            logging.error(f"Failed to schedule task at {task_time}: {e}")
            return "An error occurred while trying to schedule the task."

    def schedule_task_in(self, task_func, interval_seconds: int, *args, **kwargs) -> str:
        """
        Schedules a task to run once after a specific number of seconds.
        """
        def wrapper():
            task_func(*args, **kwargs)
            return schedule.CancelJob
            
        schedule.every(interval_seconds).seconds.do(wrapper)
        logging.info(f"Task '{task_func.__name__}' scheduled to run in {interval_seconds} seconds.")
        return f"Task '{task_func.__name__}' scheduled to run in {interval_seconds} seconds."

    def clear_schedule(self):
        """Clears all pending tasks from the scheduler."""
        schedule.clear()
        logging.info("All scheduled tasks have been cleared.")
