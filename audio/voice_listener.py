# File location: vidya/audio/voice_listener.py

import speech_recognition as sr
import logging

class VoiceListener:
    """
    Listens for audio input from the user's microphone.
    """
    def __init__(self, ambient_noise_duration: float = 1.0):
        self.recognizer = sr.Recognizer()
        self.ambient_noise_duration = ambient_noise_duration
        logging.info("VoiceListener initialized.")
        
    def listen_for_audio(self, timeout: int = 5, phrase_time_limit: int = 5):
        """
        Captures audio from the microphone.
        """
        with sr.Microphone() as source:
            logging.info("Calibrating for ambient noise...")
            self.recognizer.adjust_for_ambient_noise(source, duration=self.ambient_noise_duration)
            logging.info("Listening for audio...")
            
            try:
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                logging.info("Audio captured successfully.")
                return audio
            except sr.WaitTimeoutError:
                logging.warning("No speech detected within the timeout period.")
                return None
            except Exception as e:
                logging.error(f"An error occurred while listening: {e}")
                return None
