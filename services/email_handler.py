# File location: vidya/services/email_handler.py

import smtplib
import ssl
from email.mime.text import MIMEText
import logging

class EmailHandler:
    """
    Handles sending emails for notifications, OTPs, etc.
    """
    def __init__(self, email_address: str, email_password: str):
        self.email_address = email_address
        self.email_password = email_password
        logging.info("EmailHandler initialized.")

    def send_email(self, receiver_email: str, subject: str, body: str) -> bool:
        """
        Sends an email to the specified receiver.
        """
        if not all([self.email_address, self.email_password, receiver_email]):
            logging.error("Missing email credentials or receiver address.")
            return False
            
        message = MIMEText(body)
        message["Subject"] = subject
        message["From"] = self.email_address
        message["To"] = receiver_email
        
        context = ssl.create_default_context()
        
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(self.email_address, self.email_password)
                server.sendmail(self.email_address, receiver_email, message.as_string())
            logging.info(f"Email sent successfully to {receiver_email}.")
            return True
        except Exception as e:
            logging.error(f"Failed to send email to {receiver_email}: {e}")
            return False
