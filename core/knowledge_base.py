# File location: vidya/core/knowledge_base.py

import logging
from vidya.services.supabase_handler import SupabaseHandler
from vidya.data_processing.data_cleaner import DataCleaner

class KnowledgeBase:
    """
    Manages Vidya's knowledge by interacting with the database
    and cleaning data.
    """
    def __init__(self, supabase_handler: SupabaseHandler):
        self.supabase_handler = supabase_handler
        self.data_cleaner = DataCleaner()
        logging.info("KnowledgeBase initialized.")
        
    def ingest_data(self, source_url: str, raw_content: str):
        """
        Cleans and stores new data from a source (e.g., the web crawler).
        """
        cleaned_content = self.data_cleaner.clean_text(raw_content)
        return self.supabase_handler.insert_crawled_data(source_url, cleaned_content)

    def search_knowledge(self, query: str) -> str:
        """
        Searches the knowledge base for relevant information based on a query.
        """
        cleaned_query = self.data_cleaner.clean_text(query)
        results = self.supabase_handler.search_crawled_data(cleaned_query)
        
        if not results:
            return "I could not find any information on that topic in my knowledge base."
            
        # Concatenate and format the results for the AI model
        formatted_results = ""
        for item in results:
            formatted_results += f"Source URL: {item.get('source_url')}\nContent: {item.get('content')}\n\n"
        
        return formatted_results
