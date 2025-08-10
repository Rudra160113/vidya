# File location: vidya/backend/web_interface_router.py

import logging
from aiohttp import web
from vidya.backend.http_server import HTTPServer
from vidya.backend.static_file_handler import StaticFileHandler

class WebInterfaceRouter:
    """
    Defines and manages the routes for the web-based user interface.
    """
    def __init__(self, http_server: HTTPServer, static_file_handler: StaticFileHandler):
        self.http_server = http_server
        self.static_file_handler = static_file_handler
        logging.info("WebInterfaceRouter initialized.")

    def setup_routes(self):
        """
        Registers all routes with the aiohttp web server.
        """
        # API Routes
        self.http_server.app.router.add_post('/api/query', self.handle_query)
        self.http_server.app.router.add_get('/api/status', self.handle_status)
        
        # Static File Routes (e.g., for serving a frontend)
        self.http_server.app.router.add_get('/', self.static_file_handler.serve_index)
        self.http_server.app.router.add_static('/static/', path='vidya/client/static')
        
        logging.info("Routes have been set up.")

    async def handle_query(self, request):
        """
        Handles an incoming user query via a POST request.
        """
        try:
            data = await request.json()
            query_text = data.get('text', '')
            user_id = data.get('user_id', 'anonymous')
            
            logging.info(f"Received query from '{user_id}': {query_text}")
            
            # Placeholder for the actual AI response logic
            response_text = f"Received your query: '{query_text}'. I will process this shortly."
            
            return web.json_response({'response': response_text, 'user_id': user_id})
        except Exception as e:
            logging.error(f"Error handling query request: {e}")
            return web.json_response({'error': 'Invalid request'}, status=400)
    
    async def handle_status(self, request):
        """
        Provides a simple status check for the API.
        """
        status_info = {
            "status": "online",
            "message": "Vidya AI is up and running."
        }
        return web.json_response(status_info)
