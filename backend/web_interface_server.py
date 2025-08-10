# File location: vidya/backend/web_interface_server.py

import logging
from aiohttp import web
from vidya.backend.http_server import HTTPServer
from vidya.backend.web_interface_router import WebInterfaceRouter
from vidya.backend.static_file_handler import StaticFileHandler
from vidya.config.configuration_manager import ConfigurationManager
from vidya.core.dependency_injector import DependencyInjector

class WebInterfaceServer:
    """
    The main server for the web-based user interface.
    """
    def __init__(self, config_manager: ConfigurationManager, dependency_injector: DependencyInjector):
        self.config_manager = config_manager
        self.injector = dependency_injector
        self.host = self.config_manager.get('web_host', '0.0.0.0')
        self.port = self.config_manager.get('web_port', 5000)
        
        # Get dependencies
        self.http_server = self.injector.get('http_server')
        self.static_file_handler = self.injector.get('static_file_handler')
        
        # The router needs to be instantiated after the server and static handler
        self.router = WebInterfaceRouter(self.http_server, self.static_file_handler)
        
        logging.info("WebInterfaceServer initialized.")

    async def start(self):
        """
        Starts the aiohttp web server.
        """
        logging.info(f"Starting web server on http://{self.host}:{self.port}")
        
        # Setup routes before starting
        self.router.setup_routes()
        
        # Start the server
        runner = web.AppRunner(self.http_server.app)
        await runner.setup()
        site = web.TCPSite(runner, self.host, self.port)
        await site.start()
        
        logging.info("Web server started successfully.")

    def stop(self):
        """Stops the web server gracefully."""
        # aiohttp handles this well, but we can add a placeholder for future logic
        logging.info("Web server is stopping...")
