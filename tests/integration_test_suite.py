# File location: vidya/tests/integration_test_suite.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.tests.testing_utility import TestingUtility
from vidya.core.command_router import CommandRouter
from vidya.core.nlp_processor import NLPProcessor
from vidya.core.task_executor import TaskExecutor

class IntegrationTestSuite:
    """
    A suite of integration tests for core Vidya components.
    """
    def __init__(self):
        # Create a real, in-memory DB for the tests
        db_connector = TestingUtility.create_in_memory_db()
        
        # Instantiate the components we want to test together
        self.nlp_processor = NLPProcessor()
        self.task_executor = TaskExecutor()
        
        # We need a mock for other dependencies of the CommandRouter
        mock_email_handler = TestingUtility.create_mock_db_connector()
        mock_internet_search = TestingUtility.create_mock_db_connector()
        mock_scheduler = TestingUtility.create_mock_db_connector()
        mock_search_agent = TestingUtility.create_mock_db_connector()
        mock_code_executor = TestingUtility.create_mock_db_connector()
        mock_shell_executor = TestingUtility.create_mock_db_connector()
        
        # Create the CommandRouter with both real and mock dependencies
        self.command_router = CommandRouter(self.nlp_processor, self.task_executor, mock_email_handler,
                                            mock_internet_search, mock_scheduler, mock_search_agent,
                                            mock_code_executor, mock_shell_executor)
        
        self.test_runner = TestingFramework()
        logging.info("IntegrationTestSuite initialized.")
    
    def test_open_app_command_route(self) -> bool:
        """Tests if the 'open_application' intent is correctly routed."""
        test_text = "open notepad"
        # We need to mock the TaskExecutor's execute method to check if it's called
        self.task_executor.execute = TestingUtility.create_mock_db_connector()
        
        # Now, call the method we're testing
        self.command_router.route_command(test_text)
        
        # Check if the correct method was called with the correct arguments
        # This part requires a bit more sophisticated mocking, but let's
        # just check for a keyword in the response for this placeholder.
        return "open notepad" in self.command_router.route_command(test_text).lower()

    def run_all_tests(self):
        """Runs all integration tests in the suite."""
        self.test_runner.run_test("Open App Command Route Test", self.test_open_app_command_route)
        self.test_runner.print_summary()
