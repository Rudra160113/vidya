# File location: vidya/main.py

import logging
import asyncio
import os
from flask import Flask, send_from_directory
from threading import Thread

# Import all other necessary Vidya AI components
from vidya.core.dependency_injector import DependencyInjector
from vidya.core.command_router import CommandRouter
from vidya.core.event_dispatcher import EventDispatcher
from vidya.core.message_queue import MessageQueue
from vidya.networking.websocket_server import WebSocketServer
from vidya.plugins.plugin_manager import PluginManager
from vidya.services.gemini_service import GeminiService
from vidya.services.web_search_service import WebSearchService
from vidya.services.supabase_service import SupabaseService
from vidya.config.configuration_manager import ConfigurationManager
from vidya.security.api_key_manager import APIKeyManager
from vidya.security.security_manager import SecurityManager
from vidya.utils.logger_config import setup_logging
from vidya.audio.speech_to_text_google import SpeechToTextGoogle
from vidya.audio.text_to_speech_google import TextToSpeechGoogle

# --- Flask App Configuration ---
app = Flask(__name__, static_folder="frontend", static_url_path="")

@app.route("/")
def serve_index():
    """Serve the main index.html file."""
    return send_from_directory(app.static_folder, "index.html")

# --- Vidya AI Initialization (unchanged) ---
def init_app():
    # ... (the rest of the init_app function remains the same as before)
    setup_logging()
    logging.info("Starting Vidya AI application...")
    
    injector = DependencyInjector()
    config_manager = ConfigurationManager()
    injector.register(ConfigurationManager, config_manager)
    
    security_manager = SecurityManager(injector.get(ConfigurationManager))
    injector.register(SecurityManager, security_manager)
    
    api_key_manager = APIKeyManager(injector.get(SecurityManager), injector.get(ConfigurationManager))
    api_key_manager.load_keys()
    injector.register(APIKeyManager, api_key_manager)
    
    router = CommandRouter()
    injector.register(CommandRouter, router)
    
    message_queue = MessageQueue()
    injector.register(MessageQueue, message_queue)
    
    dispatcher = EventDispatcher()
    injector.register(EventDispatcher, dispatcher)
    
    injector.register(GeminiService, GeminiService)
    injector.register(WebSearchService, WebSearchService)
    injector.register(SupabaseService, SupabaseService)
    injector.register(SpeechToTextGoogle, SpeechToTextGoogle)
    injector.register(TextToSpeechGoogle, TextToSpeechGoogle)
    
    plugin_manager = PluginManager(injector, router)
    plugin_manager.load_plugins()
    
    logging.info("All application components initialized and services registered.")
    return injector, message_queue, router, dispatcher

async def main_loop(websocket_server, message_queue, router, dispatcher):
    """
    The main asynchronous loop for the application.
    """
    logging.info("Starting application main loop.")
    await websocket_server.start_server()

def run_websocket_server(loop, server):
    """Function to run the asyncio loop in a separate thread."""
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(server.start_server())
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()

def main():
    """The main entry point of the application."""
    injector, message_queue, router, dispatcher = init_app()
    
    host = injector.get(ConfigurationManager).get("websocket_host", "0.0.0.0")
    websocket_port = injector.get(ConfigurationManager).get("websocket_port", 8765)
    flask_port = injector.get(ConfigurationManager).get("flask_port", 5000) # Assuming a Flask port in config
    
    websocket_server = WebSocketServer(message_queue, host, websocket_port)
    
    # Start the WebSocket server in a separate thread
    ws_loop = asyncio.new_event_loop()
    ws_thread = Thread(target=run_websocket_server, args=(ws_loop, websocket_server), daemon=True)
    ws_thread.start()
    
    # Start the Flask web server in the main thread
    logging.info(f"Flask web server listening on http://{host}:{flask_port}")
    app.run(host=host, port=flask_port, debug=True, use_reloader=False)

if __name__ == "__main__":
    main()
    
