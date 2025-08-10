# File location: vidya/services/email_notification_service.py

import logging
import smtplib
from email.mime.text import MIMEText
from vidya.config.configuration_manager import ConfigurationManager

class EmailNotificationService:
    """
    A service for sending email notifications.
    """
    def __init__(self, config_manager: ConfigurationManager):
        self.config_manager = config_manager
        self.smtp_server = self.config_manager.get('smtp_server', 'smtp.gmail.com')
        self.smtp_port = self.config_manager.get('smtp_port', 587)
        self.smtp_user = self.config_manager.get('smtp_user')
        self.smtp_password = self.config_manager.get('smtp_password')
        logging.info("EmailNotificationService initialized.")

    def send_email(self, recipient: str, subject: str, body: str) -> bool:
        """
        Sends an email to a specified recipient.
        """
        if not self.smtp_user or not self.smtp_password:
            logging.error("SMTP credentials are not configured. Cannot send email.")
            return False
            
        try:
            msg = MIMEText(body)
            msg['Subject'] = subject
            msg['From'] = self.smtp_user
            msg['To'] = recipient
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()  # Secure the connection
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            
            logging.info(f"Email sent successfully to {recipient}.")
            return True
        except Exception as e:
            logging.error(f"Failed to send email to {recipient}: {e}")
            return False
