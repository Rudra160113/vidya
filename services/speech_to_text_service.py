# File location: vidya/services/speech_to_text_service.py

import logging
from vidya.config.configuration_manager import ConfigurationManager
from vidya.security.api_key_manager import APIKeyManager
import openai

class SpeechToTextService:
    """
    A service for converting speech to text.
    Uses the OpenAI Whisper API as a powerful and flexible option.
    """
    def __init__(self, config_manager: ConfigurationManager, api_key_manager: APIKeyManager):
        self.config_manager = config_manager
        self.api_key_manager = api_key_manager
        self._setup_api_client()
        logging.info("SpeechToTextService initialized.")

    def _setup_api_client(self):
        """Sets up the OpenAI API client using the API key manager."""
        openai_key = self.api_key_manager.get_key('openai')
        if openai_key:
            openai.api_key = openai_key
            logging.info("OpenAI API key loaded for STT.")
        else:
            logging.error("OpenAI API key not found. STT functionality will be disabled.")
            
    def transcribe_audio(self, audio_file_path: str) -> str | None:
        """
        Transcribes an audio file into text.
        """
        if not openai.api_key:
            return None
            
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = openai.Audio.transcribe("whisper-1", audio_file)
            
            logging.info("Audio transcribed successfully.")
            return transcript['text']
            
        except Exception as e:
            logging.error(f"Error transcribing audio file: {e}")
            return None
