# File location: vidya/data_processing/data_cleaner.py

import re
import string
import logging

class DataCleaner:
    """
    Provides methods for cleaning and preprocessing raw text data.
    """
    def __init__(self):
        logging.info("DataCleaner initialized.")

    def clean_text(self, text: str) -> str:
        """
        Performs a series of cleaning operations on a text string.
        """
        if not isinstance(text, str):
            logging.warning("Input is not a string. Returning empty string.")
            return ""
            
        text = text.lower()  # Convert to lowercase
        text = self._remove_urls(text)
        text = self._remove_html_tags(text)
        text = self._remove_punctuation(text)
        text = self._remove_extra_whitespace(text)
        return text

    def _remove_html_tags(self, text: str) -> str:
        """Removes HTML tags from a string."""
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)

    def _remove_urls(self, text: str) -> str:
        """Removes URLs from a string."""
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.sub(r'', text)

    def _remove_punctuation(self, text: str) -> str:
        """Removes all punctuation from a string."""
        return text.translate(str.maketrans('', '', string.punctuation))

    def _remove_extra_whitespace(self, text: str) -> str:
        """Removes extra whitespace and newlines, replacing with a single space."""
        text = re.sub(r'\s+', ' ', text).strip()
        return text
