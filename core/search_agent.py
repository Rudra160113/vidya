# File location: vidya/core/search_agent.py

import logging
from vidya.services.internet_search import InternetSearch
from vidya.services.web_parser import WebParser
from vidya.features.content_creator import ContentCreator

class SearchAgent:
    """
    An autonomous agent that can perform multi-step internet searches
    and synthesize information to answer complex queries.
    """
    def __init__(self, internet_search: InternetSearch, web_parser: WebParser, content_creator: ContentCreator):
        self.internet_search = internet_search
        self.web_parser = web_parser
        self.content_creator = content_creator
        logging.info("SearchAgent initialized.")

    def run_query(self, query: str) -> str:
        """
        Executes a search query, retrieves the top results, and synthesizes an answer.
        """
        logging.info(f"Running search agent for query: '{query}'")
        
        # Step 1: Initial search
        search_results = self.internet_search.search(query)
        if not search_results:
            return "I couldn't find any relevant information on the internet."
            
        full_content = ""
        # Step 2: Fetch content from top results
        for result in search_results:
            try:
                page_content = self.web_parser.parse_page(result['link'])
                full_content += page_content + "\n\n"
            except Exception as e:
                logging.warning(f"Could not parse content from {result['link']}: {e}")
                
        if not full_content:
            return "I found some links, but I couldn't extract any meaningful content."
            
        # Step 3: Use the AI to synthesize the content into a final answer
        prompt = f"Based on the following content, please provide a concise and clear answer to the question: '{query}'\n\nContent:\n{full_content}"
        final_answer = self.content_creator.vidya_brain.process_input(prompt, 'system') # Using a system user_id
        
        logging.info("Search agent successfully synthesized a final answer.")
        return final_answer
