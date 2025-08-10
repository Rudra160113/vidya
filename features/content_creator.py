# File location: vidya/features/content_creator.py

import logging

class ContentCreator:
    """
    Generates various types of content using the AI's core capabilities.
    """
    def __init__(self, vidya_brain):
        self.vidya_brain = vidya_brain
        logging.info("ContentCreator initialized.")

    def summarize_text(self, text_to_summarize: str, user_id: str) -> str:
        """
        Summarizes a given text using the AI model.
        """
        prompt = f"Please provide a concise summary of the following text: '{text_to_summarize}'"
        summary = self.vidya_brain.process_input(prompt, user_id)
        logging.info("Text summarized successfully.")
        return summary

    def write_email(self, recipient: str, subject: str, body_prompt: str, user_id: str) -> str:
        """
        Drafts an email based on a prompt.
        """
        prompt = f"Write a professional email to {recipient} with the subject '{subject}'. The body should be about: '{body_prompt}'"
        email_body = self.vidya_brain.process_input(prompt, user_id)
        
        # Format the output into a readable email structure
        email_draft = f"To: {recipient}\nSubject: {subject}\n\n{email_body}"
        logging.info("Email drafted successfully.")
        return email_draft

    def generate_social_media_post(self, topic: str, user_id: str) -> str:
        """
        Generates a social media post on a given topic.
        """
        prompt = f"Write a short, engaging social media post about: '{topic}'"
        post = self.vidya_brain.process_input(prompt, user_id)
        logging.info("Social media post generated successfully.")
        return post
