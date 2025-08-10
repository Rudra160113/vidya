# File location: vidya/services/email_sender.py

import smtplib
import ssl
import logging
from email.message import EmailMessage

class EmailSender:
    """
    Handles sending emails via an SMTP server.
    """
    def __init__(self, smtp_server: str, port: int, email_address: str, email_password: str):
        self.smtp_server = smtp_server
        self.port = port
        self.email_address = email_address
        self.email_password = email_password
        logging.info("EmailSender initialized.")
        
    def send_email(self, recipient: str, subject: str, body: str) -> str:
        """
        Sends a single email.
        """
        try:
            msg = EmailMessage()
            msg.set_content(body)
            msg['Subject'] = subject
            msg['From'] = self.email_address
            msg['To'] = recipient
            
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL(self.smtp_server, self.port, context=context) as smtp:
                smtp.login(self.email_address, self.email_password)
                smtp.send_message(msg)
                
            logging.info(f"Email sent successfully to {recipient}.")
            return f"Email to {recipient} sent successfully."
        except Exception as e:
            logging.error(f"Failed to send email: {e}")
            return f"An error occurred while sending the email: {e}"
