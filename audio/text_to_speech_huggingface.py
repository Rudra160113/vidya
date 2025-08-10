# File location: vidya/audio/text_to_speech_huggingface.py

import logging
from transformers import pipeline
import soundfile as sf
import torch

class TextToSpeechHuggingFace:
    """
    Synthesizes speech from text using a Hugging Face model.
    """
    def __init__(self, model_name: str = "suno/bark-small"):
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self._setup_pipeline()
        logging.info("TextToSpeechHuggingFace initialized.")

    def _setup_pipeline(self):
        """Sets up the Hugging Face text-to-speech pipeline."""
        try:
            self.tts_pipeline = pipeline("text-to-speech", model=self.model_name, device=self.device)
            logging.info(f"Hugging Face TTS pipeline loaded with model '{self.model_name}' on device '{self.device}'.")
        except Exception as e:
            logging.error(f"Failed to load Hugging Face TTS model '{self.model_name}': {e}")
            self.tts_pipeline = None

    def synthesize_speech(self, text: str, output_path: str) -> str | None:
        """
        Synthesizes speech from a text string and saves it to a file.

        Args:
            text (str): The text to be converted to speech.
            output_path (str): The file path to save the audio to (e.g., "output.wav").

        Returns:
            str | None: The path to the saved audio file on success, None on failure.
        """
        if not self.tts_pipeline:
            return None

        try:
            # The pipeline returns an audio dictionary
            result = self.tts_pipeline(text)
            
            # Save the audio data to a WAV file
            sf.write(output_path, result["audio"], result["sampling_rate"])
            
            logging.info(f"Speech synthesized and saved to '{output_path}'.")
            return output_path
        except Exception as e:
            logging.error(f"Error synthesizing speech with Hugging Face: {e}")
            return None
