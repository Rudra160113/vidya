# File location: vidya/services/web_crawler.py

import requests
from bs4 import BeautifulSoup
import logging
from urllib.parse import urljoin, urlparse
from collections import deque
from vidya.services.supabase_handler import SupabaseHandler

class WebCrawler:
    """
    A simple web crawler to collect data for Vidya's knowledge base.
    """
    def __init__(self, supabase_handler: SupabaseHandler):
        self.supabase_handler = supabase_handler
        self.crawled_urls = set()
        self.crawl_queue = deque()
        logging.info("WebCrawler initialized.")

    def crawl(self, start_url: str = 'https://www.example.com', max_depth: int = 2):
        """
        Starts the web crawling process from a given URL.
        """
        logging.info(f"Starting web crawl from {start_url} with max depth {max_depth}.")
        
        if start_url not in self.crawled_urls:
            self.crawl_queue.append((start_url, 0))
            self.crawled_urls.add(start_url)
        
        while self.crawl_queue:
            url, depth = self.crawl_queue.popleft()
            
            if depth > max_depth:
                continue

            try:
                response = requests.get(url, timeout=5)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # Extract and store page content
                    text_content = soup.get_text(separator=' ', strip=True)
                    self.supabase_handler.insert_crawled_data(url, text_content)

                    # Find new links to crawl
                    if depth < max_depth:
                        for link in soup.find_all('a', href=True):
                            absolute_url = urljoin(url, link['href'])
                            
                            # Filter for same domain and uncrawled links
                            if urlparse(absolute_url).netloc == urlparse(start_url).netloc and absolute_url not in self.crawled_urls:
                                self.crawl_queue.append((absolute_url, depth + 1))
                                self.crawled_urls.add(absolute_url)
                                logging.info(f"Found new link: {absolute_url}")

            except requests.exceptions.RequestException as e:
                logging.error(f"Failed to crawl {url}: {e}")
            
        logging.info("Web crawl finished.")
