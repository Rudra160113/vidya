# File location: vidya/services/internet_search.py

import logging
import requests
from vidya.config.api_key_manager import APIKeyManager

class InternetSearch:
    """
    Performs internet searches using a search engine API.
    """
    def __init__(self, api_key_manager: APIKeyManager):
        self.api_key_manager = api_key_manager
        self.api_key = self.api_key_manager.get_key("Google Search_API_KEY")
        self.cse_id = self.api_key_manager.get_key("Google Search_CSE_ID")
        self.search_url = "https://www.googleapis.com/customsearch/v1"
        logging.info("InternetSearch initialized.")

    def search(self, query: str) -> list:
        """
        Executes a search query and returns the results.
        """
        if not self.api_key or not self.cse_id:
            logging.error("Google Search API keys are not configured.")
            return []
            
        params = {
            "key": self.api_key,
            "cx": self.cse_id,
            "q": query,
            "num": 5  # Number of results to return
        }
        
        try:
            response = requests.get(self.search_url, params=params, timeout=10)
            response.raise_for_status()
            results = response.json()
            
            if 'items' in results:
                formatted_results = []
                for item in results['items']:
                    formatted_results.append({
                        "title": item.get('title', ''),
                        "link": item.get('link', ''),
                        "snippet": item.get('snippet', '')
                    })
                logging.info(f"Successfully performed search for '{query}'.")
                return formatted_results
            else:
                logging.warning(f"No search results found for '{query}'.")
                return []
        except requests.exceptions.RequestException as e:
            logging.error(f"Error during internet search for '{query}': {e}")
            return []
