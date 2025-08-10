# File location: vidya/networking/websocket_client.py

import logging
import asyncio
import websockets
import json
from typing import Dict, Any
from vidya.core.message_queue import MessageQueue

class WebSocketClient:
    """
    A client for connecting to a WebSocket server and handling messages.
    """
    def __init__(self, uri: str, message_queue: MessageQueue):
        self.uri = uri
        self.message_queue = message_queue
        self.websocket = None
        self.is_connected = False
        logging.info(f"WebSocketClient initialized for URI: {uri}")

    async def connect(self):
        """Establishes a connection to the WebSocket server."""
        try:
            self.websocket = await websockets.connect(self.uri)
            self.is_connected = True
            logging.info("WebSocket connection established.")
        except Exception as e:
            logging.error(f"Failed to connect to WebSocket server: {e}")
            self.is_connected = False

    async def disconnect(self):
        """Closes the connection to the WebSocket server."""
        if self.websocket:
            await self.websocket.close()
            self.is_connected = False
            logging.info("WebSocket connection closed.")

    async def _receive_loop(self):
        """Continuously listens for incoming messages."""
        try:
            while self.is_connected:
                message = await self.websocket.recv()
                data = json.loads(message)
                self.message_queue.put_message(data)
                logging.debug(f"Received message: {data}")
        except websockets.exceptions.ConnectionClosedError:
            logging.warning("WebSocket connection closed unexpectedly.")
        except asyncio.CancelledError:
            logging.info("WebSocket receive loop cancelled.")
        except Exception as e:
            logging.error(f"Error in WebSocket receive loop: {e}")
        finally:
            self.is_connected = False

    async def send_message(self, message: Dict[str, Any]):
        """Sends a message to the WebSocket server."""
        if self.is_connected and self.websocket:
            try:
                await self.websocket.send(json.dumps(message))
                logging.debug(f"Sent message: {message}")
            except Exception as e:
                logging.error(f"Failed to send message: {e}")
        else:
            logging.warning("Cannot send message, WebSocket not connected.")
