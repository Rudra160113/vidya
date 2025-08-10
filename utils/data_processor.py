# File location: vidya/utils/data_processor.py

import logging
from typing import Any, Dict, List

class DataProcessor:
    """
    A utility class for sanitizing, validating, and transforming data.
    """
    def __init__(self):
        logging.info("DataProcessor initialized.")

    def sanitize_string(self, text: str) -> str:
        """Removes leading/trailing whitespace and normalizes text."""
        if not isinstance(text, str):
            logging.warning(f"Sanitize string called with non-string type: {type(text)}")
            return ""
        return text.strip()

    def validate_dict_keys(self, data: Dict, required_keys: List[str]) -> bool:
        """Checks if a dictionary contains all the required keys."""
        if not isinstance(data, dict):
            logging.warning(f"Validate dict keys called with non-dict type: {type(data)}")
            return False
        
        return all(key in data for key in required_keys)
        
    def get_safe_value(self, data: Dict, key: str, default: Any = None) -> Any:
        """
        Safely retrieves a value from a dictionary, returning a default
        if the key is not found.
        """
        if not isinstance(data, dict):
            logging.warning(f"Get safe value called with non-dict type: {type(data)}")
            return default
            
        return data.get(key, default)

    def transform_to_snake_case(self, data: Dict) -> Dict:
        """Transforms dictionary keys from camelCase to snake_case."""
        if not isinstance(data, dict):
            return data
            
        transformed_data = {}
        for key, value in data.items():
            new_key = ''.join(['_' + c.lower() if c.isupper() else c for c in key]).lstrip('_')
            transformed_data[new_key] = value
            
        return transformed_data
