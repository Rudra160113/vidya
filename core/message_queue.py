# File location: vidya/core/message_queue.py

import logging
import queue
from typing import Any, Dict

class MessageQueue:
    """
    A thread-safe message queue for asynchronous communication.
    """
    def __init__(self):
        self._queue = queue.Queue()
        logging.info("MessageQueue initialized.")

    def put_message(self, message: Dict[str, Any]):
        """
        Puts a message onto the queue.
        
        Args:
            message (Dict[str, Any]): The message to be queued.
        """
        try:
            self._queue.put(message)
            logging.debug("Message put onto the queue.")
        except Exception as e:
            logging.error(f"Failed to put message onto the queue: {e}")

    def get_message(self, block: bool = True, timeout: float | None = None) -> Dict | None:
        """
        Retrieves a message from the queue.
        
        Args:
            block (bool): Whether to block until an item is available.
            timeout (float | None): Time to wait for a message.
            
        Returns:
            Dict | None: The message from the queue, or None on timeout.
        """
        try:
            message = self._queue.get(block=block, timeout=timeout)
            self._queue.task_done()
            logging.debug("Message retrieved from the queue.")
            return message
        except queue.Empty:
            logging.warning("Queue is empty, no message retrieved.")
            return None
        except Exception as e:
            logging.error(f"Failed to get message from the queue: {e}")
            return None
            
    def qsize(self) -> int:
        """Returns the number of messages currently in the queue."""
        return self._queue.qsize()
