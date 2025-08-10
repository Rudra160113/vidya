# File location: vidya/tests/testing_performance_profiler.py

import cProfile
import pstats
import io
import logging
import time

class TestingPerformanceProfiler:
    """
    Profiles the performance of a function or code block.
    """
    def __init__(self):
        logging.info("TestingPerformanceProfiler initialized.")
    
    def profile_function(self, func, *args, **kwargs):
        """
        Profiles the execution of a function and prints the results.
        """
        logging.info(f"Profiling function '{func.__name__}'...")
        
        pr = cProfile.Profile()
        pr.enable()
        
        result = func(*args, **kwargs)
        
        pr.disable()
        
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats()
        
        logging.info(f"--- Performance Profile for '{func.__name__}' ---")
        logging.info(s.getvalue())
        
        return result
    
    @staticmethod
    def simple_timer(func):
        """
        A simple decorator to measure the execution time of a function.
        """
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            logging.info(f"Function '{func.__name__}' took {end_time - start_time:.4f} seconds to execute.")
            return result
        return wrapper
