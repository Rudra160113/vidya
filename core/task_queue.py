# File location: vidya/core/task_queue.py

import queue
import threading
import logging

class TaskQueue:
    """
    A thread-safe queue for managing tasks to be processed asynchronously.
    """
    def __init__(self):
        self._queue = queue.Queue()
        self._worker_thread = None
        self._running = False
        logging.info("TaskQueue initialized.")

    def start_worker(self, worker_func):
        """Starts a worker thread to process tasks from the queue."""
        if self._running:
            logging.warning("Worker is already running.")
            return
            
        self._running = True
        self._worker_thread = threading.Thread(target=self._worker_loop, args=(worker_func,), daemon=True)
        self._worker_thread.start()
        logging.info("TaskQueue worker thread started.")

    def _worker_loop(self, worker_func):
        """The main loop for the worker thread."""
        while self._running:
            try:
                task = self._queue.get(timeout=1)
                worker_func(task)
                self._queue.task_done()
            except queue.Empty:
                continue
            except Exception as e:
                logging.error(f"Error processing task: {e}")
                self._queue.task_done()
    
    def add_task(self, task):
        """Adds a new task to the queue."""
        self._queue.put(task)
        logging.debug("Task added to queue.")
        
    def stop_worker(self):
        """Stops the worker thread and waits for all tasks to be completed."""
        if not self._running:
            return
        
        self._running = False
        self._queue.join()
        if self._worker_thread:
            self._worker_thread.join()
        logging.info("TaskQueue worker thread stopped.")
