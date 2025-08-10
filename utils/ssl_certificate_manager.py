# File location: vidya/utils/ssl_certificate_manager.py

import os
import ssl
import logging

class SSLCertificateManager:
    """
    Manages the generation and loading of SSL certificates for secure connections.
    
    In a production environment, you would use certificates from a trusted
    Certificate Authority (CA). This simple implementation is for local
    development and testing.
    """
    def __init__(self, cert_dir: str = 'certs'):
        self.cert_dir = cert_dir
        if not os.path.exists(self.cert_dir):
            os.makedirs(self.cert_dir)
        logging.info("SSLCertificateManager initialized.")
        
    def get_ssl_context(self) -> ssl.SSLContext:
        """
        Loads the SSL context from certificate and key files.
        If they don't exist, this would be a place to generate them.
        """
        cert_path = os.path.join(self.cert_dir, 'cert.pem')
        key_path = os.path.join(self.cert_dir, 'key.pem')
        
        if not os.path.exists(cert_path) or not os.path.exists(key_path):
            logging.warning("SSL certificates not found. Using a simple, insecure context.")
            # In a real app, you would generate a self-signed cert here or raise an error
            return None
        
        try:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(certfile=cert_path)
            ssl_context.load_private_key(keyfile=key_path)
            logging.info("SSL context loaded successfully.")
            return ssl_context
        except Exception as e:
            logging.error(f"Failed to load SSL certificates: {e}")
            return None
