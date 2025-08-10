# File location: vidya/core/conversation_service.py

import logging
from typing import List, Dict, Any

class ConversationService:
    """
    Manages the state and history of a user's conversation.
    """
    def __init__(self):
        # A dictionary to hold conversation history for multiple users
        self.conversations: Dict[str, List[Dict[str, Any]]] = {}
        logging.info("ConversationService initialized.")

    def get_history(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Retrieves the conversation history for a specific user.
        
        Args:
            user_id (str): The unique identifier for the user.
            
        Returns:
            List[Dict[str, Any]]: The list of conversation entries.
        """
        return self.conversations.get(user_id, [])

    def add_message(self, user_id: str, role: str, content: str):
        """
        Adds a new message to the conversation history.
        
        Args:
            user_id (str): The unique identifier for the user.
            role (str): The role of the message sender (e.g., "user", "assistant").
            content (str): The content of the message.
        """
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        
        self.conversations[user_id].append({"role": role, "content": content})
        logging.info(f"Message added to conversation for user '{user_id}'.")

    def clear_history(self, user_id: str):
        """
        Clears the entire conversation history for a user.
        """
        if user_id in self.conversations:
            del self.conversations[user_id]
            logging.info(f"Conversation history cleared for user '{user_id}'.")

    def get_context(self, user_id: str, n_messages: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieves the last n messages to provide conversational context.
        """
        history = self.get_history(user_id)
        return history[-n_messages:]
