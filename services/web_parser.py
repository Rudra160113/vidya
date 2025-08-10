# File location: vidya/services/web_parser.py

import requests
from bs4 import BeautifulSoup
import logging
from vidya.data_processing.data_cleaner import DataCleaner

class WebParser:
    """
    Parses a given URL to extract specific content based on HTML tags.
    """
    def __init__(self):
        self.data_cleaner = DataCleaner()
        logging.info("WebParser initialized.")

    def parse_page(self, url: str) -> str:
        """
        Fetches the content of a URL and extracts all text from it,
        then cleans the text.
        """
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract text from the body and clean it
                body_text = soup.body.get_text(separator=' ', strip=True) if soup.body else ""
                cleaned_text = self.data_cleaner.clean_text(body_text)
                
                logging.info(f"Successfully parsed and cleaned content from {url}.")
                return cleaned_text
            else:
                logging.warning(f"Failed to fetch {url}. Status code: {response.status_code}")
                return ""
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching page {url}: {e}")
            return ""

    def find_all_links(self, url: str) -> list:
        """
        Finds all anchor tags (links) on a page.
        """
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                links = [a['href'] for a in soup.find_all('a', href=True)]
                return links
            return []
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching page to find links {url}: {e}")
            return []
