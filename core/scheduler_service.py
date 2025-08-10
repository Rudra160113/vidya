# File location: vidya/core/scheduler_service.py

import logging
from datetime import datetime
from vidya.data.database_connector import DatabaseConnector
import json

class SchedulerService:
    """
    Manages the scheduling of tasks to be run in the future.
    """
    def __init__(self, db_connector: DatabaseConnector):
        self.db_connector = db_connector
        self._setup_table()
        logging.info("SchedulerService initialized.")
        
    def _setup_table(self):
        """Creates the scheduled_tasks table if it doesn't exist."""
        create_table = """
        CREATE TABLE IF NOT EXISTS scheduled_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_type TEXT NOT NULL,
            task_data TEXT NOT NULL,
            run_at DATETIME NOT NULL,
            is_completed INTEGER DEFAULT 0
        );
        """
        self.db_connector.execute_query(create_table)
        logging.info("Scheduled tasks table verified/created.")

    def schedule_task(self, task_type: str, task_data: dict, run_at: datetime) -> str:
        """
        Schedules a new task to be executed at a specific time.
        `task_data` is a dictionary of parameters for the task.
        """
        try:
            task_data_json = json.dumps(task_data)
            insert_query = "INSERT INTO scheduled_tasks (task_type, task_data, run_at) VALUES (?, ?, ?)"
            self.db_connector.execute_query(insert_query, (task_type, task_data_json, run_at.isoformat()))
            logging.info(f"Task '{task_type}' scheduled for {run_at.isoformat()}.")
            return "Task scheduled successfully."
        except Exception as e:
            logging.error(f"Failed to schedule task: {e}")
            return "An error occurred while scheduling the task."
            
    def get_pending_tasks(self) -> list:
        """
        Retrieves all tasks that are due to be run now or in the past.
        """
        now = datetime.now().isoformat()
        query = "SELECT id, task_type, task_data FROM scheduled_tasks WHERE run_at <= ? AND is_completed = 0"
        results = self.db_connector.execute_query(query, (now,))
        
        pending_tasks = []
        for task_id, task_type, task_data_json in results:
            pending_tasks.append({
                "id": task_id,
                "task_type": task_type,
                "task_data": json.loads(task_data_json)
            })
            
        return pending_tasks
