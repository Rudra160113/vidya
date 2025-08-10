# File location: vidya/tests/testing_main.py

import logging
import unittest.mock
import sys
import threading
from vidya.tests.testing_framework import TestingFramework

# Import the main script and patch its dependencies
from vidya import main

class TestingMain:
    """
    A suite of tests to verify the correct initialization and execution of main.py.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        logging.info("TestingMain initialized.")
    
    @unittest.mock.patch('vidya.main.ConfigurationManager')
    @unittest.mock.patch('vidya.main.setup_logging')
    @unittest.mock.patch('vidya.main.GeminiService')
    @unittest.mock.patch('vidya.main.WebSocketServer')
    def test_main_initialization(self, mock_websocket_server, mock_gemini_service, mock_setup_logging, mock_config_manager) -> bool:
        """Tests if the main function initializes core components correctly."""
        # Mock the configuration manager to return a non-None value
        mock_config_manager.return_value.get.return_value = 'mock-key'

        # We'll use a threading.Event to control the asyncio loop
        mock_loop_stop_event = threading.Event()
        
        # Mock the asyncio.run to be able to exit it gracefully for the test
        with unittest.mock.patch('asyncio.run', side_effect=lambda coroutine: mock_loop_stop_event.set()):
            
            # Since the `main` function runs a blocking `asyncio.run`, we'll
            # need to run it in a separate thread.
            main_thread = threading.Thread(target=main.main)
            main_thread.start()
            
            # Wait for the mocked asyncio.run to be called
            mock_loop_stop_event.wait(timeout=1)
            
            # Check if logging was set up
            mock_setup_logging.assert_called_once()
            
            # Check if Gemini service was initialized
            mock_gemini_service.assert_called_once()
            
            # Check if the WebSocket server was started
            mock_websocket_server.return_value.start_server.assert_called_once()

            # Clean up the thread
            main_thread.join()
            
            return True
        
    def run_all_tests(self):
        """Runs all main application tests."""
        self.test_runner.run_test("Main Initialization Test", self.test_main_initialization)
        self.test_runner.print_summary()
