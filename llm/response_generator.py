# File location: vidya/llm/response_generator.py

import logging
from typing import Any

class ResponseGenerator:
    """
    Generates a final, human-readable response from the result of a command.
    """
    def __init__(self):
        logging.info("ResponseGenerator initialized.")
    
    def generate(self, result: Any) -> str:
        """
        Formats a command result into a user-friendly response.
        
        Args:
            result (Any): The output from a command execution, which can be
                          a string, list, dictionary, or other data types.
                          
        Returns:
            str: The formatted response string.
        """
        if isinstance(result, str):
            return result
        
        if isinstance(result, list):
            if not result:
                return "There are no items to list."
            
            list_items = "\n- " + "\n- ".join(map(str, result))
            return f"Here are your items:{list_items}"
            
        if isinstance(result, dict):
            # Handle a structured error response
            if result.get("status") == "error":
                return f"I'm sorry, I encountered an error: {result.get('message', 'An unknown error occurred.')}"
            
            # Handle a dictionary of key-value pairs
            formatted_items = "\n".join([f"{key}: {value}" for key, value in result.items()])
            return f"Here is the information:\n{formatted_items}"
            
        # Fallback for unrecognized formats
        logging.warning(f"ResponseGenerator received an unrecognized result format: {type(result)}")
        return "I'm sorry, I couldn't understand that result."
