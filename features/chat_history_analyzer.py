# File location: vidya/features/chat_history_analyzer.py

import logging
from collections import Counter
from vidya.data.chat_history import ChatHistory

class ChatHistoryAnalyzer:
    """
    Analyzes chat history to identify trends and user behavior.
    """
    def __init__(self, chat_history: ChatHistory):
        self.chat_history = chat_history
        logging.info("ChatHistoryAnalyzer initialized.")
        
    def get_most_frequent_commands(self, user_id: str, num_commands: int = 5) -> list:
        """
        Analyzes a user's chat history to find their most frequent commands.
        This uses simple keyword matching for a placeholder implementation.
        """
        logging.info(f"Analyzing chat history for user '{user_id}'...")
        
        history = self.chat_history.get_history(user_id)
        
        if not history:
            return []
            
        # Simple keyword-based command extraction
        commands = [self._extract_command(item.get('message', '')) for item in history if item.get('sender') == 'user']
        
        # Count the frequency of each extracted command
        command_counts = Counter(commands)
        most_common = command_counts.most_common(num_commands)
        
        logging.info(f"Most frequent commands for user '{user_id}': {most_common}")
        return most_common

    def _extract_command(self, text: str) -> str:
        """
        A simple, rule-based method to extract a command from a message.
        """
        text = text.lower().strip()
        if text.startswith("open"):
            return "open"
        if text.startswith("search"):
            return "search"
        if text.startswith("send email"):
            return "send email"
        return "other"
