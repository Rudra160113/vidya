# File location: vidya/utils/http_client.py

import logging
import requests
from typing import Any, Dict, Tuple

class HttpClient:
    """
    A simple, centralized HTTP client for making API requests.
    """
    def __init__(self, timeout: int = 10):
        self.timeout = timeout
        logging.info("HttpClient initialized.")

    def get(self, url: str, params: Dict[str, Any] = None, headers: Dict[str, Any] = None) -> Tuple[Dict | None, int]:
        """Performs a GET request."""
        try:
            response = requests.get(url, params=params, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.Timeout:
            logging.error(f"HTTP GET request to {url} timed out.")
            return None, 408
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP GET request to {url} failed: {e}")
            return None, getattr(e.response, 'status_code', 500)
        except Exception as e:
            logging.error(f"An unexpected error occurred during HTTP GET to {url}: {e}")
            return None, 500

    def post(self, url: str, data: Dict[str, Any] = None, headers: Dict[str, Any] = None) -> Tuple[Dict | None, int]:
        """Performs a POST request."""
        try:
            response = requests.post(url, json=data, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            return response.json(), response.status_code
        except requests.exceptions.Timeout:
            logging.error(f"HTTP POST request to {url} timed out.")
            return None, 408
        except requests.exceptions.RequestException as e:
            logging.error(f"HTTP POST request to {url} failed: {e}")
            return None, getattr(e.response, 'status_code', 500)
        except Exception as e:
            logging.error(f"An unexpected error occurred during HTTP POST to {url}: {e}")
            return None, 500
