# File location: vidya/backend/http_server.py

from flask import Flask, request, jsonify
import logging

class HTTPServer:
    """
    A simple HTTP server to expose Vidya's core functionality via a REST API.
    """
    def __init__(self, vidya_brain, port: int = 5000):
        self.app = Flask(__name__)
        self.vidya_brain = vidya_brain
        self.port = port
        self._setup_routes()
        logging.info(f"HTTPServer initialized on port {self.port}.")

    def _setup_routes(self):
        """Defines the API routes for the server."""
        @self.app.route('/api/query', methods=['POST'])
        def query_api():
            data = request.get_json()
            if not data or 'text' not in data or 'user_id' not in data:
                return jsonify({"error": "Invalid request format"}), 400
                
            text = data['text']
            user_id = data['user_id']
            
            try:
                response = self.vidya_brain.process_input(text, user_id)
                return jsonify({"response": response}), 200
            except Exception as e:
                logging.error(f"API query failed: {e}")
                return jsonify({"error": "An internal error occurred"}), 500
                
    def run(self):
        """Starts the Flask server."""
        try:
            self.app.run(port=self.port, debug=False)
        except Exception as e:
            logging.error(f"Failed to run HTTP server: {e}")
