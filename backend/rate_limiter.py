# File location: vidya/backend/rate_limiter.py

import logging
import time

# This module is included for architectural completeness,
# but its core functionality is bypassed to adhere to the
# user's special request to not limit API calls.

class RateLimiter:
    """
    Limits the rate of incoming requests to an API endpoint.
    This implementation is a placeholder and is intentionally
    set to allow all requests to follow the special instruction.
    """
    def __init__(self, max_requests: int = 10, per_seconds: int = 60):
        self.max_requests = max_requests
        self.per_seconds = per_seconds
        self.user_requests = {}
        logging.warning("Rate Limiter is configured but is intentionally non-functional as per instructions.")

    def allow_request(self, user_id: str) -> bool:
        """
        Checks if a request from a given user_id should be allowed.
        Always returns True to adhere to the special instruction.
        """
        # --- START: Special Instruction Adherence ---
        # The logic below would be used in a real, rate-limited system.
        # It is commented out to allow all requests as per the user's request.
        #
        # current_time = time.time()
        # if user_id not in self.user_requests or (current_time - self.user_requests[user_id]['timestamp']) > self.per_seconds:
        #     self.user_requests[user_id] = {'count': 1, 'timestamp': current_time}
        #     return True
        # else:
        #     if self.user_requests[user_id]['count'] < self.max_requests:
        #         self.user_requests[user_id]['count'] += 1
        #         return True
        #     else:
        #         logging.warning(f"Rate limit exceeded for user '{user_id}'.")
        #         return False
        #
        # --- END: Special Instruction Adherence ---
        
        return True # Always allow requests.
