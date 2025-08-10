# File location: vidya/backend/websocket_handler.py

import asyncio
import websockets
import json
import logging

class WebSocketHandler:
    """
    Handles real-time, bidirectional communication using WebSockets.
    """
    def __init__(self, vidya_brain, host: str = 'localhost', port: int = 8765):
        self.vidya_brain = vidya_brain
        self.host = host
        self.port = port
        self.connected_clients = set()
        logging.info(f"WebSocketHandler initialized on ws://{self.host}:{self.port}.")

    async def register(self, websocket):
        """Adds a new client to the connected set."""
        self.connected_clients.add(websocket)
        logging.info(f"New WebSocket client connected. Total clients: {len(self.connected_clients)}")

    async def unregister(self, websocket):
        """Removes a client from the connected set."""
        self.connected_clients.remove(websocket)
        logging.info(f"WebSocket client disconnected. Total clients: {len(self.connected_clients)}")

    async def handle_message(self, websocket, path):
        """
        Handles incoming messages from a WebSocket client.
        """
        await self.register(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    text = data.get('text')
                    user_id = data.get('user_id', 'websocket_user')
                    
                    if text:
                        logging.info(f"Received message from '{user_id}': '{text}'")
                        response = self.vidya_brain.process_input(text, user_id)
                        
                        response_message = {"type": "response", "content": response}
                        await websocket.send(json.dumps(response_message))
                        
                except json.JSONDecodeError:
                    logging.warning("Received non-JSON message.")
                    await websocket.send(json.dumps({"error": "Invalid JSON format"}))
        finally:
            await self.unregister(websocket)
            
    def run(self):
        """Starts the WebSocket server."""
        try:
            start_server = websockets.serve(self.handle_message, self.host, self.port)
            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()
        except Exception as e:
            logging.error(f"Failed to run WebSocket server: {e}")
