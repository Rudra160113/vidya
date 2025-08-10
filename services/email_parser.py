# File location: vidya/services/email_parser.py

import imaplib
import email
import logging
import ssl

class EmailParser:
    """
    Reads and parses emails from a user's inbox using IMAP.
    """
    def __init__(self, email_address: str, email_password: str):
        self.email_address = email_address
        self.email_password = email_password
        self.imap_server = "imap.gmail.com"
        logging.info("EmailParser initialized.")

    def fetch_unread_emails(self) -> list:
        """
        Connects to the inbox and fetches unread emails.
        """
        try:
            context = ssl.create_default_context()
            with imaplib.IMAP4_SSL(self.imap_server, 993, context=context) as imap:
                imap.login(self.email_address, self.email_password)
                imap.select("inbox")
                status, messages = imap.search(None, "UNSEEN")
                
                email_list = []
                for num in messages[0].split():
                    status, data = imap.fetch(num, "(RFC822)")
                    msg = email.message_from_bytes(data[0][1])
                    
                    email_info = {
                        "from": msg.get("From"),
                        "subject": msg.get("Subject"),
                        "body": self._get_email_body(msg)
                    }
                    email_list.append(email_info)
                    
                logging.info(f"Successfully fetched {len(email_list)} unread emails.")
                return email_list
        except Exception as e:
            logging.error(f"Error fetching emails: {e}")
            return []

    def _get_email_body(self, msg):
        """
        Extracts the plain text body from an email message.
        """
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdispo = str(part.get("Content-Disposition"))
                if ctype == "text/plain" and "attachment" not in cdispo:
                    return part.get_payload(decode=True).decode()
        else:
            return msg.get_payload(decode=True).decode()
        return ""
