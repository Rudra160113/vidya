# File location: vidya/features/text_to_image_processor.py

import logging
from vidya.core.nlp_processor import NLPProcessor

class TextToImageProcessor:
    """
    Refines and processes natural language text into a structured prompt
    for an image generation model.
    """
    def __init__(self, nlp_processor: NLPProcessor):
        self.nlp_processor = nlp_processor
        logging.info("TextToImageProcessor initialized.")
        
    def generate_prompt(self, text: str) -> str:
        """
        Takes a raw text input and turns it into a detailed prompt
        for an image generator.
        """
        # Step 1: Extract keywords and entities
        extracted_entities = self.nlp_processor.extract_entities(text)
        
        # Step 2: Use Vidya's core brain to expand on the prompt
        # This part would use the LLM to add artistic detail, style, and composition
        prompt = f"Create a detailed, high-quality image of: {text}. "
        
        # This is a placeholder for a more complex LLM interaction
        # For example, we could ask the LLM to suggest artistic styles.
        if "in the style of" not in text.lower():
            prompt += "Please generate this in a photorealistic, cinematic style."
        
        logging.info(f"Generated a refined image prompt: '{prompt}'")
        return prompt
