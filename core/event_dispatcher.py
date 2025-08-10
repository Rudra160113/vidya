# File location: vidya/core/event_dispatcher.py

import logging
from collections import defaultdict
from typing import Callable, Any, Dict

class EventDispatcher:
    """
    Manages the registration and dispatching of events.
    """
    def __init__(self):
        self._handlers = defaultdict(list)
        logging.info("EventDispatcher initialized.")

    def register_handler(self, event_type: str, handler: Callable):
        """
        Registers a handler function to be called when a specific event occurs.
        
        Args:
            event_type (str): The type of event to listen for.
            handler (Callable): The function to call when the event is dispatched.
        """
        self._handlers[event_type].append(handler)
        logging.debug(f"Handler registered for event type: {event_type}")

    def dispatch_event(self, event_type: str, event_data: Dict[str, Any]):
        """
        Dispatches an event, calling all registered handlers for that event type.
        
        Args:
            event_type (str): The type of event to dispatch.
            event_data (Dict[str, Any]): A dictionary containing the event data.
        """
        if event_type in self._handlers:
            for handler in self._handlers[event_type]:
                try:
                    handler(event_data)
                except Exception as e:
                    logging.error(f"Error calling handler for event '{event_type}': {e}", exc_info=True)
        else:
            logging.warning(f"No handlers registered for event type: {event_type}")
