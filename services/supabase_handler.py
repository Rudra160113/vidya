# File location: vidya/services/supabase_handler.py

from supabase import create_client, Client
import logging
import datetime
import json

class SupabaseHandler:
    """
    Handles connection and interaction with multiple Supabase projects.
    """
    def __init__(self, config_file: str):
        self.clients = []
        self.next_client_index = 0
        self.load_clients_from_config(config_file)

    def load_clients_from_config(self, config_file: str):
        """Loads credentials from a JSON file and creates Supabase clients."""
        try:
            with open(config_file, 'r') as f:
                configs = json.load(f)
            
            for config in configs:
                url = config.get("url")
                key = config.get("key")
                if url and key:
                    try:
                        client: Client = create_client(url, key)
                        # Optional: Authenticate if needed for RLS
                        # client.auth.sign_in_with_password({'email': 'your_email@example.com', 'password': 'your_password'})
                        self.clients.append(client)
                        logging.info(f"Connected to Supabase project at {url}")
                    except Exception as e:
                        logging.error(f"Failed to connect to Supabase at {url}: {e}")
            
            if not self.clients:
                raise ValueError("No valid Supabase clients were created.")

        except FileNotFoundError:
            raise FileNotFoundError(f"Supabase config file not found at '{config_file}'.")
        except json.JSONDecodeError:
            raise ValueError(f"Invalid JSON in config file '{config_file}'.")
    
    def get_next_client(self):
        """Returns the next client in a round-robin fashion for balanced load."""
        if not self.clients:
            return None
        client = self.clients[self.next_client_index]
        self.next_client_index = (self.next_client_index + 1) % len(self.clients)
        return client

    def log_interaction(self, user_id: str, source: str, message: str):
        """
        Stores a chat interaction in one of the Supabase projects.
        """
        client = self.get_next_client()
        if not client:
            return "Error: No Supabase connections."

        data = {
            "user_id": user_id,
            "source": source,
            "message": message
        }
        try:
            client.table('history').insert(data).execute()
            logging.info(f"Interaction logged to Supabase project: {source} said '{message}'")
            return "Interaction logged."
        except Exception as e:
            logging.error(f"Failed to log interaction: {e}")
            return "Error logging interaction."

    def get_history(self, user_id: str) -> list:
        """
        Retrieves all chat history for a specific user ID from all projects.
        """
        all_history = []
        for client in self.clients:
            try:
                response = client.table('history').select('*').eq('user_id', user_id).order('created_at').execute()
                all_history.extend(response.data)
            except Exception as e:
                logging.error(f"Failed to retrieve history from a Supabase project: {e}")
        
        # Sort and return the combined history
        all_history.sort(key=lambda x: x['created_at'])
        return all_history
        
    def store_otp(self, user_id: str, email: str, otp: str):
        """Stores a generated OTP in a single Supabase project."""
        client = self.get_next_client()
        if not client:
            return False
            
        expires_at = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=25)
        data = {
            "user_id": user_id,
            "email": email,
            "otp": otp,
            "expires_at": expires_at.isoformat()
        }
        
        try:
            client.table('otps').insert(data).execute()
            logging.info(f"OTP stored for user '{user_id}'.")
            return True
        except Exception as e:
            logging.error(f"Failed to store OTP: {e}")
            return False
            
    def verify_otp(self, user_id: str, otp: str):
        """Verifies an OTP against a Supabase project."""
        # We need a consistent way to find the OTP, so we will check all projects
        for client in self.clients:
            try:
                response = client.table('otps').select('*').eq('user_id', user_id).order('created_at', desc=True).limit(1).execute()
                otp_record = response.data[0] if response.data else None
                
                if otp_record and otp_record['otp'] == otp:
                    expires_at = datetime.datetime.fromisoformat(otp_record['expires_at'])
                    if datetime.datetime.now(datetime.timezone.utc) < expires_at:
                        client.table('otps').delete().eq('id', otp_record['id']).execute()
                        return True
            except Exception as e:
                logging.error(f"Failed to verify OTP in a Supabase project: {e}")
        return False

    def insert_crawled_data(self, url: str, content: str):
        """Inserts a crawled data entry into one of the Supabase projects."""
        client = self.get_next_client()
        if not client:
            return False
            
        data = {
            "source_url": url,
            "content": content
        }
        try:
            client.table('crawled_data').insert(data).execute()
            logging.info(f"Crawled data from {url} inserted into Supabase project.")
            return True
        except Exception as e:
            logging.error(f"Failed to insert crawled data: {e}")
            return False

    def search_crawled_data(self, query: str):
        """Searches the crawled data for a specific query across all projects."""
        all_results = []
        for client in self.clients:
            try:
                response = client.table('crawled_data').select('*').ilike('content', f"%{query}%").execute()
                all_results.extend(response.data)
            except Exception as e:
                logging.error(f"Failed to search crawled data in a Supabase project: {e}")
        
        return all_results
