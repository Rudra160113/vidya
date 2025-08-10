# File location: vidya/data/data_retrieval.py

import logging
from vidya.data.database_connector import DatabaseConnector

class DataRetrieval:
    """
    Manages the retrieval of data from the internal knowledge base.
    """
    def __init__(self, db_connector: DatabaseConnector):
        self.db_connector = db_connector
        logging.info("DataRetrieval initialized.")

    def search_knowledge_base(self, keyword: str) -> list:
        """
        Searches the knowledge base table for content containing a specific keyword.
        """
        query = "SELECT source_url, content FROM knowledge_base WHERE content LIKE ? LIMIT 5"
        results = self.db_connector.execute_query(query, (f'%{keyword}%',))
        
        if not results:
            logging.info(f"No results found for keyword: '{keyword}'.")
            return []
            
        formatted_results = []
        for row in results:
            formatted_results.append({
                "source_url": row[0],
                "content": row[1]
            })
            
        logging.info(f"Found {len(formatted_results)} results for keyword: '{keyword}'.")
        return formatted_results

    def get_user_history(self, user_id: str, limit: int = 10) -> list:
        """
        Retrieves the last N interactions for a specific user.
        """
        query = "SELECT source, message FROM history WHERE user_id = ? ORDER BY created_at DESC LIMIT ?"
        results = self.db_connector.execute_query(query, (user_id, limit))
        
        if not results:
            logging.info(f"No history found for user: '{user_id}'.")
            return []
            
        formatted_history = []
        for row in results:
            formatted_history.append({
                "source": row[0],
                "message": row[1]
            })
            
        logging.info(f"Retrieved {len(formatted_history)} history entries for user: '{user_id}'.")
        return formatted_history
