# File location: vidya/backend/web_interface_handler.py

import logging
from aiohttp import web
from vidya.core.dependency_injector import DependencyInjector
from vidya.backend.web_socket_server import WebSocketServer

class WebInterfaceHandler:
    """
    Handles HTTP requests for the web interface, serving static files and
    routing API calls to the appropriate backend services.
    """
    def __init__(self, app: web.Application, injector: DependencyInjector):
        self.app = app
        self.injector = injector
        self.websocket_server = self.injector.get(WebSocketServer)
        
        # Register routes
        self.app.router.add_static('/static/', path='vidya/web/static', name='static')
        self.app.router.add_get('/', self.handle_root)
        self.app.router.add_post('/api/command', self.handle_command)
        
        logging.info("WebInterfaceHandler initialized.")

    async def handle_root(self, request: web.Request) -> web.Response:
        """Serves the main index.html file."""
        return web.FileResponse('vidya/web/index.html')

    async def handle_command(self, request: web.Request) -> web.Response:
        """
        Handles incoming command requests from the web client.
        This is a placeholder for a more complex command processing pipeline.
        """
        try:
            data = await request.json()
            user_input = data.get('input', '')
            user_id = data.get('user_id', 'anonymous')
            
            logging.info(f"Received command from '{user_id}': {user_input}")
            
            # Here, we would typically process the command using the CommandExecutor
            # and other services. For now, we'll just send a placeholder response.
            response_text = f"Command '{user_input}' received. Processing..."
            
            # Broadcast the response back to all connected clients
            await self.websocket_server.broadcast(f"Response for {user_id}: {response_text}")
            
            return web.json_response({"status": "success", "message": response_text})
        
        except Exception as e:
            logging.error(f"Error handling command request: {e}")
            return web.json_response({"status": "error", "message": "Failed to process command."}, status=500)
