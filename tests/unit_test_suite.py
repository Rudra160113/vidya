# File location: vidya/tests/unit_test_suite.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.data.database_connector import DatabaseConnector

class UnitTestSuite:
    """
    A suite of unit tests for core Vidya components.
    """
    def __init__(self):
        self.db_connector = DatabaseConnector(db_path=':memory:') # Use in-memory DB for tests
        self.db_connector.setup_database()
        self.test_runner = TestingFramework()
        logging.info("UnitTestSuite initialized.")
    
    def test_database_connection(self) -> bool:
        """Test if the database connector can connect and create a table."""
        try:
            # We already connected in __init__
            self.db_connector.execute_query("INSERT INTO history (user_id, source, message) VALUES (?, ?, ?)", 
                                            ("test_user", "test_source", "test_message"))
            results = self.db_connector.execute_query("SELECT message FROM history WHERE user_id=?", ("test_user",))
            return results[0][0] == "test_message"
        except Exception as e:
            logging.error(f"Database connection test failed: {e}")
            return False

    def run_all_tests(self):
        """Runs all tests in the suite."""
        self.test_runner.run_test("Database Connection Test", self.test_database_connection)
        
        # Add more tests here
        # self.test_runner.run_test("NLP Processor Test", self.test_nlp_processor)
        # self.test_runner.run_test("Email Handler Test", self.test_email_handler)

        self.test_runner.print_summary()
        self.db_connector.close()
