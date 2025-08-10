# File location: vidya/nlp/command_parser.py

import logging

class CommandParser:
    """
    Parses the output from the NLP Processor into a standardized command dictionary.
    """
    def __init__(self):
        logging.info("CommandParser initialized.")
        
    def parse_nlp_output(self, nlp_output: dict) -> dict:
        """
        Takes the NLP output and extracts a command and its arguments.
        
        Args:
            nlp_output (dict): The dictionary returned by the NLP processor.
                               Expected to contain a 'text' and 'entities' key.
                               
        Returns:
            dict: A dictionary in the format {'name': 'command_name', 'args': {...}}.
        """
        command_name = nlp_output.get('entities', {}).get('command', 'unknown')
        
        # Extract arguments by removing the command key from the entities
        args = nlp_output.get('entities', {}).copy()
        if 'command' in args:
            del args['command']
            
        return {
            'name': command_name,
            'args': args
        }
