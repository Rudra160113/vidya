# File location: vidya/tests/testing_web_socket_server.py

import logging
import unittest.mock
from aiohttp import web, WSMsgType, WSCloseCode
from vidya.tests.testing_framework import TestingFramework
from vidya.backend.web_socket_server import WebSocketServer

class TestingWebSocketServer:
    """
    A suite of tests to verify the functionality of the WebSocketServer.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.app = web.Application()
        self.server = WebSocketServer(self.app)
        logging.info("TestingWebSocketServer initialized.")

    @unittest.mock.patch('aiohttp.web.WebSocketResponse')
    async def test_websocket_handler(self, mock_ws_response) -> bool:
        """Tests if the handler can accept a connection and process a message."""
        mock_ws = unittest.mock.AsyncMock()
        mock_ws_response.return_value = mock_ws
        
        # Simulate an incoming message
        mock_msg = unittest.mock.Mock()
        mock_msg.type = WSMsgType.TEXT
        mock_msg.data = "Test message"
        
        # Simulate the async for loop
        mock_ws.__aiter__.return_value = [mock_msg]
        
        # Create a mock request
        mock_request = unittest.mock.Mock()
        
        await self.server.websocket_handler(mock_request)
        
        # Check if the connection was prepared and the message was sent back
        mock_ws.prepare.assert_called_once_with(mock_request)
        mock_ws.send_str.assert_called_once_with("Server received: Test message")
        
        return len(self.server.ws_connections) == 0 # Connection should be removed after loop finishes

    async def test_broadcast_message(self) -> bool:
        """Tests if a message is broadcasted to all connected clients."""
        # Setup mock connections
        mock_ws1 = unittest.mock.AsyncMock()
        mock_ws2 = unittest.mock.AsyncMock()
        self.server.ws_connections.append(mock_ws1)
        self.server.ws_connections.append(mock_ws2)
        
        message_to_send = "Broadcast test"
        await self.server.broadcast(message_to_send)
        
        # Verify that the message was sent to both connections
        mock_ws1.send_str.assert_called_once_with(message_to_send)
        mock_ws2.send_str.assert_called_once_with(message_to_send)
        
        return True # The test passes if no exceptions are raised

    async def run_all_tests(self):
        """Runs all WebSocket server tests."""
        # Since these are async tests, we need to run them inside an event loop
        await self.test_runner.run_async_test("WebSocket Handler Test", self.test_websocket_handler)
        await self.test_runner.run_async_test("Broadcast Message Test", self.test_broadcast_message)
        self.test_runner.print_summary()
