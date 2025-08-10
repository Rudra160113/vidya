# File location: vidya/tests/testing_websocket_server.py

import logging
import unittest.mock
import asyncio
import json
from vidya.tests.testing_framework import TestingFramework
from vidya.networking.websocket_server import WebSocketServer
from vidya.core.message_queue import MessageQueue

class TestingWebSocketServer:
    """
    A suite of tests to verify the functionality of the WebSocketServer.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup mock dependencies
        self.mock_message_queue = unittest.mock.Mock(spec=MessageQueue)
        self.server = WebSocketServer(self.mock_message_queue, host="localhost", port=8001)
        logging.info("TestingWebSocketServer initialized.")
    
    @unittest.mock.patch('websockets.serve')
    def test_start_server(self, mock_serve) -> bool:
        """Tests if the server starts correctly."""
        async def mock_serve_coroutine():
            pass

        mock_serve.return_value = mock_serve_coroutine()
        
        async def test_coroutine():
            await self.server.start_server()
            mock_serve.assert_called_once_with(self.server._handler, "localhost", 8001)

        asyncio.run(test_coroutine())
        
        return True

    @unittest.mock.patch('websockets.serve')
    def test_handle_incoming_message(self, mock_serve) -> bool:
        """Tests if the server's handler processes a message and puts it in the queue."""
        mock_websocket = unittest.mock.AsyncMock()
        mock_websocket.recv.side_effect = ["{\"type\": \"command\", \"data\": \"hello\"}", asyncio.CancelledError]
        
        async def test_coroutine():
            # Call the handler directly to test its logic
            await self.server._handler(mock_websocket, "path")
            
            # Verify the message was put on the queue
            self.mock_message_queue.put_message.assert_called_once_with(
                {'type': 'command', 'data': 'hello'}
            )
            
        asyncio.run(test_coroutine())

        return True

    def run_all_tests(self):
        """Runs all websocket server tests."""
        self.test_runner.run_test("Start Server Test", self.test_start_server)
        self.test_runner.run_test("Handle Incoming Message Test", self.test_handle_incoming_message)
        self.test_runner.print_summary()
