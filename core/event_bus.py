# File location: vidya/core/event_bus.py

import logging
import threading

class EventBus:
    """
    A simple publish/subscribe event bus for inter-component communication.
    """
    def __init__(self):
        self._subscribers = {}
        self._lock = threading.Lock()
        logging.info("EventBus initialized.")

    def subscribe(self, event_type: str, callback):
        """
        Subscribes a callback function to a specific event type.
        """
        with self._lock:
            if event_type not in self._subscribers:
                self._subscribers[event_type] = []
            self._subscribers[event_type].append(callback)
            logging.info(f"Callback '{callback.__name__}' subscribed to event '{event_type}'.")

    def publish(self, event_type: str, data: dict):
        """
        Publishes an event, notifying all subscribed callbacks.
        """
        logging.info(f"Publishing event '{event_type}' with data: {data}")
        with self._lock:
            if event_type in self._subscribers:
                for callback in self._subscribers[event_type]:
                    try:
                        callback(data)
                    except Exception as e:
                        logging.error(f"Error in event handler '{callback.__name__}' for event '{event_type}': {e}")

    def unsubscribe(self, event_type: str, callback):
        """
        Unsubscribes a callback function from an event type.
        """
        with self._lock:
            if event_type in self._subscribers and callback in self._subscribers[event_type]:
                self._subscribers[event_type].remove(callback)
                logging.info(f"Callback '{callback.__name__}' unsubscribed from event '{event_type}'.")
