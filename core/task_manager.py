# File location: vidya/core/task_manager.py

import logging
import asyncio
from typing import Callable, Any
from vidya.core.dependency_injector import DependencyInjector

class TaskManager:
    """
    Manages the lifecycle of asynchronous, long-running tasks.
    """
    def __init__(self, injector: DependencyInjector):
        self.injector = injector
        self.active_tasks = {}  # Store tasks by ID or name
        logging.info("TaskManager initialized.")
        
    async def start_task(self, task_id: str, coro: Callable, *args, **kwargs) -> bool:
        """
        Starts a new task and tracks it.
        
        Args:
            task_id (str): A unique identifier for the task.
            coro (Callable): The coroutine function to run as a task.
            *args, **kwargs: Arguments to pass to the coroutine.
            
        Returns:
            bool: True if the task was started, False otherwise.
        """
        if task_id in self.active_tasks:
            logging.warning(f"Task with ID '{task_id}' is already running.")
            return False
            
        try:
            task = asyncio.create_task(coro(*args, **kwargs))
            self.active_tasks[task_id] = task
            logging.info(f"Task '{task_id}' started.")
            return True
        except Exception as e:
            logging.error(f"Failed to start task '{task_id}': {e}")
            return False

    def get_task_status(self, task_id: str) -> str:
        """
        Gets the status of a running task.
        """
        task = self.active_tasks.get(task_id)
        if not task:
            return "Not found"
            
        if task.done():
            return "Done"
        
        return "Running"

    async def wait_for_task(self, task_id: str):
        """
        Waits for a task to complete.
        """
        task = self.active_tasks.get(task_id)
        if task:
            await task
            
    def cancel_task(self, task_id: str) -> bool:
        """
        Cancels a running task.
        """
        task = self.active_tasks.get(task_id)
        if not task:
            logging.warning(f"Task '{task_id}' not found.")
            return False
            
        task.cancel()
        del self.active_tasks[task_id]
        logging.info(f"Task '{task_id}' canceled.")
        return True
