# File location: vidya/tests/testing_docker_compose.py

import logging
import subprocess
import time
from vidya.tests.testing_framework import TestingFramework

class TestingDockerCompose:
    """
    A suite of integration tests for the docker-compose setup.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        logging.info("TestingDockerCompose initialized.")

    def test_docker_services_start(self) -> bool:
        """Tests if the docker-compose services can be started successfully."""
        logging.info("Attempting to start Docker containers with docker-compose...")
        try:
            # -f specifies the compose file, -d runs in detached mode
            command = ["docker-compose", "-f", "../../docker-compose.yml", "up", "--build", "-d"]
            subprocess.run(command, check=True, capture_output=True, text=True)
            
            # Wait for services to be ready (placeholder time)
            time.sleep(5)
            
            # Check if containers are running
            status_command = ["docker-compose", "-f", "../../docker-compose.yml", "ps", "-q"]
            output = subprocess.run(status_command, check=True, capture_output=True, text=True)
            containers_running = bool(output.stdout.strip())
            
            if not containers_running:
                logging.error("Docker containers did not start correctly.")
                return False
                
            logging.info("Docker containers started successfully.")
            return True
            
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to run docker-compose: {e.stderr}")
            return False
            
        finally:
            self._cleanup_containers()

    def _cleanup_containers(self):
        """Stops and removes the Docker containers."""
        logging.info("Cleaning up Docker containers...")
        try:
            command = ["docker-compose", "-f", "../../docker-compose.yml", "down"]
            subprocess.run(command, check=True, capture_output=True, text=True)
            logging.info("Docker containers stopped and removed.")
        except subprocess.CalledProcessError as e:
            logging.error(f"Failed to stop docker-compose: {e.stderr}")
            
    def run_all_tests(self):
        """Runs all Docker Compose-related integration tests."""
        self.test_runner.run_test("Docker Compose Services Start Test", self.test_docker_services_start)
        self.test_runner.print_summary()
