# File location: vidya/nlp/voice_command_parser.py

import logging
from vidya.nlp.nlp_processor import NLPProcessor
from vidya.core.dependency_injector import DependencyInjector

class VoiceCommandParser:
    """
    Parses transcribed voice input into a structured command dictionary.
    """
    def __init__(self, injector: DependencyInjector):
        self.nlp_processor = injector.get(NLPProcessor)
        logging.info("VoiceCommandParser initialized.")

    def parse(self, transcribed_text: str) -> dict:
        """
        Processes transcribed text and returns a command dictionary.
        
        Args:
            transcribed_text (str): The text from the speech-to-text service.
            
        Returns:
            dict: A dictionary in the format {'name': 'command_name', 'args': {...}}.
        """
        if not transcribed_text:
            return {"name": "unrecognized", "args": {"reason": "empty_input"}}
        
        try:
            # The NLPProcessor handles the heavy lifting of entity extraction
            nlp_output = self.nlp_processor.process(transcribed_text)
            
            command_name = nlp_output.get('command', 'unrecognized')
            args = nlp_output.get('entities', {})
            
            logging.info(f"Parsed command: '{command_name}' with args: {args}")
            
            return {
                "name": command_name,
                "args": args
            }
        except Exception as e:
            logging.error(f"Error parsing voice command '{transcribed_text}': {e}")
            return {"name": "error", "args": {"reason": str(e)}}
