# File location: vidya/database/database_service_supabase.py

import logging
from supabase import create_client, Client
from vidya.config.configuration_manager import ConfigurationManager
from vidya.security.api_key_manager import APIKeyManager

class DatabaseServiceSupabase:
    """
    A service for interacting with a Supabase database.
    """
    def __init__(self, config_manager: ConfigurationManager, api_key_manager: APIKeyManager):
        self.config_manager = config_manager
        self.api_key_manager = api_key_manager
        self.supabase_url = self.config_manager.get('supabase_url')
        self.supabase_key = self.api_key_manager.get_key('supabase')
        self.client: Client = self._setup_client()
        logging.info("DatabaseServiceSupabase initialized.")

    def _setup_client(self) -> Client | None:
        """Sets up the Supabase client."""
        if not self.supabase_url or not self.supabase_key:
            logging.error("Supabase credentials not configured. Database functionality is disabled.")
            return None
        
        try:
            return create_client(self.supabase_url, self.supabase_key)
        except Exception as e:
            logging.error(f"Failed to connect to Supabase: {e}")
            return None

    def insert_record(self, table: str, data: dict) -> dict | None:
        """Inserts a new record into a specified table."""
        if not self.client:
            return None
        try:
            response = self.client.from_(table).insert(data).execute()
            logging.info(f"Record inserted into '{table}'.")
            return response.data
        except Exception as e:
            logging.error(f"Failed to insert record into '{table}': {e}")
            return None

    def fetch_records(self, table: str, filters: dict = None) -> list[dict] | None:
        """Fetches records from a specified table."""
        if not self.client:
            return None
        try:
            query = self.client.from_(table).select("*")
            if filters:
                for key, value in filters.items():
                    query = query.eq(key, value)
            
            response = query.execute()
            logging.info(f"Fetched {len(response.data)} records from '{table}'.")
            return response.data
        except Exception as e:
            logging.error(f"Failed to fetch records from '{table}': {e}")
            return None
