# File location: vidya/tests/testing_websocket_client.py

import logging
import unittest.mock
import json
import asyncio
from vidya.tests.testing_framework import TestingFramework
from vidya.networking.websocket_client import WebSocketClient
from vidya.core.message_queue import MessageQueue

class TestingWebSocketClient:
    """
    A suite of tests to verify the functionality of the WebSocketClient.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup mock dependencies
        self.mock_message_queue = unittest.mock.Mock(spec=MessageQueue)
        self.client = WebSocketClient("ws://localhost:8000", self.mock_message_queue)
        logging.info("TestingWebSocketClient initialized.")
    
    @unittest.mock.patch('websockets.connect')
    def test_connect_and_send(self, mock_connect) -> bool:
        """Tests if the client can connect and send a message."""
        mock_websocket = unittest.mock.AsyncMock()
        mock_connect.return_value.__aenter__.return_value = mock_websocket
        
        async def test_coroutine():
            await self.client.connect()
            await self.client.send_message({"type": "test", "data": "hello"})
            mock_websocket.send.assert_called_once_with(json.dumps({"type": "test", "data": "hello"}))
            
            # Clean up the connection state for subsequent tests
            self.client.websocket = None
            
        asyncio.run(test_coroutine())
        
        return True # Assertion was successful

    @unittest.mock.patch('websockets.connect')
    def test_receive_message(self, mock_connect) -> bool:
        """Tests if the client can receive a message and put it on the queue."""
        mock_websocket = unittest.mock.AsyncMock()
        mock_websocket.recv.side_effect = ["{\"type\": \"response\", \"data\": \"pong\"}", asyncio.CancelledError]
        mock_connect.return_value.__aenter__.return_value = mock_websocket
        
        async def test_coroutine():
            await self.client.connect()
            # The receive loop will run until the CancelledError
            await self.client._receive_loop()
            
            self.mock_message_queue.put_message.assert_called_once_with(
                {'type': 'response', 'data': 'pong'}
            )
            
            self.client.websocket = None

        asyncio.run(test_coroutine())

        return True # Assertion was successful

    def run_all_tests(self):
        """Runs all websocket client tests."""
        self.test_runner.run_test("Connect and Send Test", self.test_connect_and_send)
        self.test_runner.run_test("Receive Message Test", self.test_receive_message)
        self.test_runner.print_summary()
