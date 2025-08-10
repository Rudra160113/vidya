# File location: vidya/utils/internet_handler.py

import requests
import logging

class InternetHandler:
    """
    Checks for internet connectivity.
    """
    def __init__(self):
        logging.info("InternetHandler initialized.")

    def check_connection(self, url: str = 'http://www.google.com/', timeout: int = 5) -> bool:
        """
        Checks for an active internet connection by attempting to
        connect to a reliable website.
        """
        try:
            requests.get(url, timeout=timeout)
            logging.info("Internet connection is active.")
            return True
        except requests.exceptions.RequestException as e:
            logging.error(f"No internet connection: {e}")
            return False
