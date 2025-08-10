# File location: vidya/backend/web_socket_server.py

import logging
import asyncio
from aiohttp import web, WSCloseCode

class WebSocketServer:
    """
    A WebSocket server to handle real-time communication with the client.
    """
    def __init__(self, app: web.Application):
        self.app = app
        self.ws_connections = []
        app.router.add_get('/ws', self.websocket_handler)
        logging.info("WebSocketServer initialized.")

    async def websocket_handler(self, request: web.Request):
        """
        Handles incoming WebSocket connections.
        """
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        
        self.ws_connections.append(ws)
        logging.info("New WebSocket connection established.")
        
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                logging.info(f"Received message from client: {msg.data}")
                # You can handle incoming messages here, e.g., process user commands
                await ws.send_str(f"Server received: {msg.data}")
            elif msg.type == web.WSMsgType.ERROR:
                logging.error(f"WebSocket connection closed with exception: {ws.exception()}")
                
        self.ws_connections.remove(ws)
        logging.info("WebSocket connection closed.")
        return ws

    async def broadcast(self, message: str):
        """
        Broadcasts a message to all connected clients.
        """
        if not self.ws_connections:
            logging.info("No active WebSocket connections to broadcast to.")
            return
            
        logging.info(f"Broadcasting message to {len(self.ws_connections)} clients.")
        
        closed_connections = []
        for ws in self.ws_connections:
            if not ws.closed:
                await ws.send_str(message)
            else:
                closed_connections.append(ws)
                
        # Clean up closed connections
        for ws in closed_connections:
            self.ws_connections.remove(ws)
