# File location: vidya/tests/testing_load_balancer.py

import requests
import concurrent.futures
import time
import logging

class TestingLoadBalancer:
    """
    Simulates a high number of concurrent users to test system performance.
    """
    def __init__(self, endpoint_url: str):
        self.endpoint_url = endpoint_url
        logging.info("TestingLoadBalancer initialized.")

    def run_stress_test(self, num_requests: int, max_workers: int = 10):
        """
        Executes a stress test by sending a specified number of requests concurrently.
        """
        logging.info(f"Starting stress test with {num_requests} requests to {self.endpoint_url}...")
        
        start_time = time.time()
        successful_requests = 0
        failed_requests = 0
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_url = {executor.submit(self._make_request, i): i for i in range(num_requests)}
            for future in concurrent.futures.as_completed(future_to_url):
                try:
                    result = future.result()
                    if result:
                        successful_requests += 1
                    else:
                        failed_requests += 1
                except Exception as e:
                    logging.error(f"Request generated an exception: {e}")
                    failed_requests += 1
        
        end_time = time.time()
        elapsed_time = end_time - start_time
        
        logging.info("--- Stress Test Results ---")
        logging.info(f"Total time: {elapsed_time:.2f} seconds")
        logging.info(f"Total requests: {num_requests}")
        logging.info(f"Successful requests: {successful_requests}")
        logging.info(f"Failed requests: {failed_requests}")
        logging.info(f"Requests per second: {num_requests / elapsed_time:.2f}")

    def _make_request(self, request_id: int):
        """Sends a single test request to the endpoint."""
        try:
            response = requests.post(
                self.endpoint_url,
                json={"text": f"Test query {request_id}", "user_id": "test_user"},
                timeout=5
            )
            response.raise_for_status()
            logging.debug(f"Request {request_id} succeeded with status {response.status_code}.")
            return True
        except requests.exceptions.RequestException as e:
            logging.warning(f"Request {request_id} failed: {e}")
            return False
