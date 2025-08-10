# File location: vidya/services/api_handler.py

import requests
import logging
import json

class APIHandler:
    """
    A generic handler for making and managing external API requests.
    """
    def __init__(self):
        logging.info("APIHandler initialized.")

    def get_data(self, url: str, params: dict = None, headers: dict = None) -> dict:
        """
        Sends a GET request to a specified URL and returns the JSON response.
        """
        try:
            response = requests.get(url, params=params, headers=headers, timeout=15)
            response.raise_for_status()  # Raises an HTTPError for bad responses (4xx or 5xx)
            logging.info(f"Successfully fetched data from URL: {url}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error making GET request to {url}: {e}")
            return {"error": str(e)}

    def post_data(self, url: str, data: dict, headers: dict = None) -> dict:
        """
        Sends a POST request to a specified URL with a JSON payload.
        """
        try:
            headers = headers or {'Content-Type': 'application/json'}
            response = requests.post(url, data=json.dumps(data), headers=headers, timeout=15)
            response.raise_for_status()
            logging.info(f"Successfully posted data to URL: {url}")
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error(f"Error making POST request to {url}: {e}")
            return {"error": str(e)}
