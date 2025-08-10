# File location: vidya/backend/static_file_handler.py

import logging
from aiohttp import web
import os

class StaticFileHandler:
    """
    Handles serving static files for the web interface.
    """
    def __init__(self, static_dir: str = 'vidya/client/static'):
        self.static_dir = static_dir
        self.index_file = os.path.join(self.static_dir, 'index.html')
        logging.info(f"StaticFileHandler initialized. Serving from '{self.static_dir}'.")

    async def serve_index(self, request):
        """
        Serves the main index.html file for the application.
        """
        if not os.path.exists(self.index_file):
            return web.Response(text="Index file not found.", status=404)
            
        with open(self.index_file, 'r') as f:
            html_content = f.read()
            
        return web.Response(text=html_content, content_type='text/html')
