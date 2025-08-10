# File location: vidya/data/database_backup.py

import logging
import os
import shutil
from datetime import datetime

class DatabaseBackup:
    """
    Performs scheduled backups of the application's database.
    """
    def __init__(self, db_path: str, backup_dir: str = 'backups'):
        self.db_path = db_path
        self.backup_dir = backup_dir
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)
        logging.info("DatabaseBackup initialized.")

    def create_backup(self):
        """
        Creates a timestamped copy of the database file.
        """
        if not os.path.exists(self.db_path):
            logging.error(f"Database file not found at {self.db_path}. Backup aborted.")
            return "Database file not found."
            
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        backup_filename = f"vidya_db_backup_{timestamp}.sqlite"
        backup_path = os.path.join(self.backup_dir, backup_filename)
        
        try:
            shutil.copyfile(self.db_path, backup_path)
            logging.info(f"Database backup created successfully at {backup_path}.")
            return f"Database backup successful. Saved to {backup_path}."
        except Exception as e:
            logging.error(f"Failed to create database backup: {e}")
            return "An error occurred while creating the database backup."

    def restore_backup(self, backup_file: str):
        """
        Restores the database from a specified backup file.
        WARNING: This will overwrite the current database.
        """
        backup_path = os.path.join(self.backup_dir, backup_file)
        if not os.path.exists(backup_path):
            logging.error(f"Backup file not found at {backup_path}. Restore aborted.")
            return "Backup file not found."

        try:
            shutil.copyfile(backup_path, self.db_path)
            logging.info(f"Database restored from {backup_path}.")
            return "Database restored successfully."
        except Exception as e:
            logging.error(f"Failed to restore database from backup: {e}")
            return "An error occurred while restoring the database."
