# File location: vidya/utils/data_sanitizer.py

import logging
import html
import re

class DataSanitizer:
    """
    Cleans and sanitizes user input to prevent security vulnerabilities.
    """
    def __init__(self):
        logging.info("DataSanitizer initialized.")

    def sanitize_html(self, text: str) -> str:
        """
        Escapes HTML characters in a string to prevent XSS attacks.
        """
        return html.escape(text)

    def sanitize_shell_command(self, command: str) -> str:
        """
        Sanitizes a command string to prevent command injection.
        This is a simple implementation and a more robust solution is needed
        for a production system.
        """
        # A very basic approach is to remove dangerous characters
        sanitized_command = re.sub(r'[;&|`$(){}<>\'\"]', '', command)
        return sanitized_command.strip()

    def sanitize_sql_query_part(self, text: str) -> str:
        """
        Sanitizes a string for use in an SQL query to prevent injection.
        Note: This is a last resort. Parameterized queries should always be used.
        """
        # A basic approach to escape single quotes
        sanitized_text = text.replace("'", "''")
        return sanitized_text
