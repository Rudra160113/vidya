# File location: vidya/core/task_scheduler.py

import logging
import time
import threading
from typing import Callable, Any
import schedule

class TaskScheduler:
    """
    Schedules and runs tasks in the background at specified intervals.
    """
    def __init__(self):
        self.scheduler = schedule.Scheduler()
        self.scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self._running = True
        self.jobs = {}
        logging.info("TaskScheduler initialized.")

    def _run_scheduler(self):
        """Internal method to run the scheduler's event loop."""
        while self._running:
            self.scheduler.run_pending()
            time.sleep(1)

    def _run_pending_jobs(self):
        """Helper to run pending jobs directly for testing purposes."""
        self.scheduler.run_pending()

    def start(self):
        """Starts the scheduler thread."""
        if not self.scheduler_thread.is_alive():
            self.scheduler_thread.start()
            logging.info("TaskScheduler thread started.")

    def stop(self):
        """Stops the scheduler thread."""
        self._running = False
        self.scheduler_thread.join()
        logging.info("TaskScheduler thread stopped.")
    
    def schedule_job(self, interval: int, job_func: Callable, *args, **kwargs) -> Any:
        """
        Schedules a job to run every 'interval' seconds.
        
        Args:
            interval (int): The number of seconds between job runs.
            job_func (Callable): The function to be executed.
            
        Returns:
            Any: The job instance returned by the scheduler.
        """
        job = self.scheduler.every(interval).seconds.do(job_func, *args, **kwargs)
        self.jobs[job.job_id] = job
        logging.info(f"Scheduled job with ID '{job.job_id}' to run every {interval} seconds.")
        return job.job_id

    def cancel_job(self, job_id: Any):
        """Cancels a scheduled job by its ID."""
        if job_id in self.jobs:
            self.scheduler.cancel_job(self.jobs[job_id])
            del self.jobs[job_id]
            logging.info(f"Canceled job with ID '{job_id}'.")
