# File location: vidya/tests/testing_framework.py

import logging

class TestingFramework:
    """
    A simple framework for running tests and reporting results.
    """
    def __init__(self):
        self.tests_run = 0
        self.tests_passed = 0
        self.tests_failed = 0
        logging.info("TestingFramework initialized.")

    def run_test(self, test_name: str, test_func, *args, **kwargs):
        """
        Runs a single test function and reports success or failure.
        The test function should return True for success and False for failure.
        """
        self.tests_run += 1
        try:
            result = test_func(*args, **kwargs)
            if result:
                logging.info(f"[PASS] {test_name}")
                self.tests_passed += 1
            else:
                logging.error(f"[FAIL] {test_name}: Test function returned False.")
                self.tests_failed += 1
        except Exception as e:
            logging.error(f"[ERROR] {test_name}: An unexpected exception occurred: {e}")
            self.tests_failed += 1

    def print_summary(self):
        """
        Prints a summary of the test run.
        """
        summary = f"\n--- Test Summary ---\n"
        summary += f"Total tests run: {self.tests_run}\n"
        summary += f"Tests passed: {self.tests_passed}\n"
        summary += f"Tests failed: {self.tests_failed}\n"
        
        if self.tests_failed == 0:
            summary += "All tests passed successfully! 🎉"
        else:
            summary += f"Some tests failed. Please check the logs. 😔"

        logging.info(summary)
