# File location: vidya/gui/gui_event_handler.py

import logging
from typing import Dict, Any
from vidya.core.message_queue import MessageQueue
from vidya.core.dependency_injector import DependencyInjector

class GUIEventHandler:
    """
    Handles events from the user interface and translates them into
    messages for the core application.
    """
    def __init__(self, injector: DependencyInjector):
        self.message_queue = injector.get(MessageQueue)
        self.supported_events = ["click", "input", "submit"]
        logging.info("GUIEventHandler initialized.")

    def handle_event(self, event_data: Dict[str, Any]):
        """
        Processes an incoming GUI event and sends it to the message queue.
        
        Args:
            event_data (Dict[str, Any]): A dictionary describing the event.
        """
        event_type = event_data.get("type")
        if event_type in self.supported_events:
            message = {
                "event_type": "gui_event",
                "event_data": event_data
            }
            self.message_queue.put_message(message)
            logging.debug(f"GUI event '{event_type}' handled and queued.")
        else:
            logging.warning(f"Unsupported GUI event type received: {event_type}")
