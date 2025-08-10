# File location: vidya/networking/websocket_server.py

import logging
import asyncio
import websockets
import json
from vidya.core.message_queue import MessageQueue

class WebSocketServer:
    """
    A server for handling incoming WebSocket connections and messages.
    """
    def __init__(self, message_queue: MessageQueue, host: str, port: int):
        self.message_queue = message_queue
        self.host = host
        self.port = port
        self.clients = set()
        logging.info(f"WebSocketServer initialized on {host}:{port}")

    async def _handler(self, websocket, path):
        """
        Handles a single WebSocket connection, adding it to the list of clients
        and listening for messages.
        """
        self.clients.add(websocket)
        logging.info(f"New client connected: {websocket.remote_address}")
        try:
            async for message in websocket:
                data = json.loads(message)
                self.message_queue.put_message(data)
                logging.debug(f"Received message from client: {data}")
        except websockets.exceptions.ConnectionClosedError as e:
            logging.warning(f"Client disconnected: {websocket.remote_address}, reason: {e}")
        finally:
            self.clients.remove(websocket)

    async def start_server(self):
        """Starts the WebSocket server."""
        try:
            async with websockets.serve(self._handler, self.host, self.port):
                await asyncio.Future()  # Run forever
        except Exception as e:
            logging.error(f"Failed to start WebSocket server: {e}")

    async def send_message(self, message: str):
        """Sends a message to all connected clients."""
        if self.clients:
            await asyncio.gather(*[client.send(message) for client in self.clients])
            logging.debug(f"Sent message to {len(self.clients)} clients: {message}")
