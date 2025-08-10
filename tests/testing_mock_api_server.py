# File location: vidya/tests/testing_mock_api_server.py

import json
import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

class MockAPIHandler(BaseHTTPRequestHandler):
    """
    Handles requests for the mock API server.
    """
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        request_data = json.loads(post_data)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        
        # Simple routing based on the request data
        response_data = {}
        if 'api_call_type' in request_data and request_data['api_call_type'] == 'weather':
            response_data = {"status": "success", "data": {"city": "Testville", "temp": "25C"}}
        elif 'api_call_type' in request_data and request_data['api_call_type'] == 'stocks':
            response_data = {"status": "success", "data": {"symbol": "TEST", "price": 100.0}}
        else:
            response_data = {"status": "error", "message": "Unknown API call type."}

        self.wfile.write(json.dumps(response_data).encode('utf-8'))

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b"Mock API Server is running.")

class MockAPIServer:
    """
    A simple mock API server for testing purposes.
    """
    def __init__(self, host: str = 'localhost', port: int = 8080):
        self.server_address = (host, port)
        self.httpd = HTTPServer(self.server_address, MockAPIHandler)
        self.server_thread = threading.Thread(target=self.httpd.serve_forever, daemon=True)
        logging.info(f"Mock API Server initialized on {host}:{port}.")
        
    def start(self):
        """Starts the mock server in a new thread."""
        self.server_thread.start()
        logging.info("Mock API Server started.")

    def stop(self):
        """Stops the mock server."""
        self.httpd.shutdown()
        self.httpd.server_close()
        self.server_thread.join()
        logging.info("Mock API Server stopped.")
