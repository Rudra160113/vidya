# File location: vidya/main.py

import logging
import asyncio
import os
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

def init_app():
    """Initializes all core application components and services."""
    
    # 1. Setup logging
    setup_logging()
    logging.info("Starting Vidya AI application...")
    
    # 2. Setup Dependency Injector
    injector = DependencyInjector()
    
    # 3. Register Core Components
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
    
    # 4. Register Services
    injector.register(GeminiService, GeminiService)
    injector.register(WebSearchService, WebSearchService)
    injector.register(SupabaseService, SupabaseService)
    injector.register(SpeechToTextGoogle, SpeechToTextGoogle)
    injector.register(TextToSpeechGoogle, TextToSpeechGoogle)
    
    # 5. Load Plugins
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
    
    # You would also have an event processing loop here
    # while True:
    #     try:
    #         message = message_queue.get_message(timeout=1)
    #         if message:
    #             # Process the message here
    #             ...
    #         await asyncio.sleep(0.1)
    #     except asyncio.CancelledError:
    #         break

def main():
    """The main entry point of the application."""
    injector, message_queue, router, dispatcher = init_app()
    
    # Get configuration for the WebSocket server
    host = injector.get(ConfigurationManager).get("websocket_host", "0.0.0.0")
    port = injector.get(ConfigurationManager).get("websocket_port", 8765)
    
    websocket_server = WebSocketServer(message_queue, host, port)
    
    # Run the main asynchronous loop
    try:
        asyncio.run(main_loop(websocket_server, message_queue, router, dispatcher))
    except KeyboardInterrupt:
        logging.info("Application shut down by user.")
    except Exception as e:
        logging.critical(f"An unrecoverable error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    main()
