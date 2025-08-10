# File location: vidya/tests/testing_ssl_manager.py

import logging
import os
import shutil
from vidya.tests.testing_framework import TestingFramework
from vidya.core.ssl_certificate_manager import SSLCertificateManager

class TestingSSLManager:
    """
    A suite of tests to verify the functionality of the SSLCertificateManager.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.certs_dir = "test_certs"
        self.domain = "test.local"
        logging.info("TestingSSLManager initialized.")

    def _setup_test_environment(self):
        """Creates a clean directory for certificates."""
        if os.path.exists(self.certs_dir):
            shutil.rmtree(self.certs_dir)
        os.makedirs(self.certs_dir)
        
    def _cleanup_test_environment(self):
        """Removes the temporary certificates directory."""
        if os.path.exists(self.certs_dir):
            shutil.rmtree(self.certs_dir)

    def test_certificate_generation(self) -> bool:
        """Tests if a self-signed certificate can be generated."""
        self._setup_test_environment()
        manager = SSLCertificateManager(self.domain, self.certs_dir)
        
        # Initially, no certificates should exist
        cert, key = manager.get_certificates()
        if cert or key:
            self._cleanup_test_environment()
            return False
            
        manager.generate_self_signed_cert()
        
        # After generation, the files should exist
        cert, key = manager.get_certificates()
        self._cleanup_test_environment()
        
        return os.path.exists(cert) and os.path.exists(key)

    def run_all_tests(self):
        """Runs all SSL manager tests."""
        self.test_runner.run_test("Certificate Generation Test", self.test_certificate_generation)
        self.test_runner.print_summary()
