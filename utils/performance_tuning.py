# File location: vidya/utils/performance_tuning.py

import logging
import functools
import time

class PerformanceTuning:
    """
    Provides utilities for tuning and optimizing application performance.
    """
    def __init__(self):
        self._cache = {}
        logging.info("PerformanceTuning initialized.")
        
    def memoize(self, func):
        """
        A simple decorator for caching function results (memoization).
        """
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            key = (func.__name__, args, frozenset(kwargs.items()))
            if key not in self._cache:
                self._cache[key] = func(*args, **kwargs)
            return self._cache[key]
        return wrapper

    def pre_load_model(self, model_loader, model_name: str, model_type: str):
        """
        Pre-loads an AI model into memory to reduce latency on first use.
        """
        start_time = time.time()
        logging.info(f"Pre-loading model '{model_name}'...")
        try:
            model_loader.load_model(model_name, model_type)
            logging.info(f"Model '{model_name}' pre-loaded in {time.time() - start_time:.2f} seconds.")
            return True
        except Exception as e:
            logging.error(f"Failed to pre-load model '{model_name}': {e}")
            return False

    def clear_cache(self):
        """Clears all cached results."""
        self._cache.clear()
        logging.info("Performance cache cleared.")
