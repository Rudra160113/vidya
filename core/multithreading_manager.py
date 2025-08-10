# File location: vidya/core/multithreading_manager.py

import logging
from concurrent.futures import ThreadPoolExecutor

class MultithreadingManager:
    """
    Manages a thread pool for executing tasks concurrently.
    """
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        logging.info(f"MultithreadingManager initialized with {max_workers} workers.")

    def run_task(self, func, *args, **kwargs):
        """
        Submits a function to be executed in a separate thread.
        Returns a Future object.
        """
        try:
            future = self.executor.submit(func, *args, **kwargs)
            return future
        except Exception as e:
            logging.error(f"Failed to submit task to thread pool: {e}")
            return None

    def shutdown(self):
        """
        Shuts down the thread pool, waiting for all tasks to complete.
        """
        self.executor.shutdown(wait=True)
        logging.info("MultithreadingManager has been shut down.")
