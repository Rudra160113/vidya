# File location: vidya/data/database_migrator.py

import logging
import os
from vidya.data.database_connector import DatabaseConnector

class DatabaseMigrator:
    """
    Manages database schema migrations using SQL files.
    """
    def __init__(self, db_connector: DatabaseConnector, migrations_dir: str = 'vidya/data/migrations'):
        self.db_connector = db_connector
        self.migrations_dir = migrations_dir
        self._setup_migrations_table()
        logging.info("DatabaseMigrator initialized.")

    def _setup_migrations_table(self):
        """Creates a table to track which migrations have been applied."""
        create_table = """
        CREATE TABLE IF NOT EXISTS applied_migrations (
            migration_id TEXT PRIMARY KEY,
            applied_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.db_connector.execute_query(create_table)
        logging.info("Applied migrations table verified/created.")

    def run_migrations(self):
        """
        Applies all pending migrations from the migrations directory.
        """
        if not os.path.exists(self.migrations_dir):
            logging.warning(f"Migrations directory '{self.migrations_dir}' not found.")
            return "Migrations directory not found."
            
        applied_migrations = self._get_applied_migrations()
        
        migration_files = sorted([f for f in os.listdir(self.migrations_dir) if f.endswith('.sql')])
        
        for migration_file in migration_files:
            migration_id = migration_file.split('.sql')[0]
            if migration_id not in applied_migrations:
                file_path = os.path.join(self.migrations_dir, migration_file)
                try:
                    with open(file_path, 'r') as f:
                        sql_script = f.read()
                    
                    self.db_connector.execute_query(sql_script)
                    self._mark_migration_as_applied(migration_id)
                    logging.info(f"Migration '{migration_file}' applied successfully.")
                except Exception as e:
                    logging.error(f"Failed to apply migration '{migration_file}': {e}")
                    raise RuntimeError(f"Migration '{migration_file}' failed.")
        
        return "All pending migrations have been applied."

    def _get_applied_migrations(self) -> set:
        """Retrieves a set of all migration IDs that have been applied."""
        query = "SELECT migration_id FROM applied_migrations"
        results = self.db_connector.execute_query(query)
        return {row[0] for row in results}

    def _mark_migration_as_applied(self, migration_id: str):
        """Inserts a record for a newly applied migration."""
        query = "INSERT INTO applied_migrations (migration_id) VALUES (?)"
        self.db_connector.execute_query(query, (migration_id,))
