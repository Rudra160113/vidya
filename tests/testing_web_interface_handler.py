# File location: vidya/tests/testing_web_interface_handler.py

import logging
import unittest.mock
from aiohttp import web, ClientSession
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from vidya.tests.testing_framework import TestingFramework
from vidya.backend.web_interface_handler import WebInterfaceHandler
from vidya.core.dependency_injector import DependencyInjector
from vidya.backend.web_socket_server import WebSocketServer

class TestingWebInterfaceHandler(AioHTTPTestCase):
    """
    A suite of tests to verify the functionality of the WebInterfaceHandler.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_runner = TestingFramework()
        logging.info("TestingWebInterfaceHandler initialized.")
    
    async def get_application(self):
        """Create and return the web application for testing."""
        app = web.Application()
        injector = DependencyInjector()
        mock_websocket_server = unittest.mock.AsyncMock(spec=WebSocketServer)
        injector.register(WebSocketServer, mock_websocket_server)
        WebInterfaceHandler(app, injector)
        return app
    
    @unittest_run_loop
    async def test_handle_root(self):
        """Tests if the root route serves the main page."""
        resp = await self.client.get('/')
        assert resp.status == 200
        # Check if the response is likely an HTML file
        text = await resp.text()
        assert "<html>" in text

    @unittest.mock.patch('aiohttp.test_utils.AioHTTPTestCase.get_application')
    @unittest.mock.patch('vidya.backend.web_interface_handler.WebInterfaceHandler.handle_command')
    @unittest_run_loop
    async def test_handle_command(self, mock_handle_command, mock_get_application):
        """Tests if the command API endpoint is called correctly."""
        # The mock handler should return a mock response
        mock_response = web.json_response({"status": "success"})
        mock_handle_command.return_value = mock_response
        
        resp = await self.client.post('/api/command', json={'input': 'hello'})
        
        assert resp.status == 200
        data = await resp.json()
        assert data['status'] == 'success'
        
        mock_handle_command.assert_called_once()
        
    def run_all_tests(self):
        """Runs all web interface handler tests."""
        # AioHTTPTestCase has its own test discovery
        pass
