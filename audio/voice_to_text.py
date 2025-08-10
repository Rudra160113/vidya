# File location: vidya/audio/voice_to_text.py

import speech_recognition as sr
import logging

class VoiceToText:
    """
    Converts audio data into a text string using various speech recognition services.
    """
    def __init__(self):
        self.recognizer = sr.Recognizer()
        logging.info("VoiceToText initialized.")

    def transcribe_audio(self, audio_data) -> str:
        """
        Transcribes audio data into text using the Google Web Speech API.
        """
        if not audio_data:
            return ""
            
        try:
            text = self.recognizer.recognize_google(audio_data)
            logging.info(f"Transcription successful: '{text}'")
            return text
        except sr.UnknownValueError:
            logging.warning("Could not understand the audio.")
            return "unknown_value_error"
        except sr.RequestError as e:
            logging.error(f"Could not request results from Google Speech Recognition service; {e}")
            return "request_error"
        except Exception as e:
            logging.error(f"An unexpected error occurred during transcription: {e}")
            return "transcription_error"

    def transcribe_audio_from_file(self, audio_file_path: str) -> str:
        """
        Transcribes an audio file into text.
        """
        try:
            with sr.AudioFile(audio_file_path) as source:
                audio_data = self.recognizer.record(source)
                return self.transcribe_audio(audio_data)
        except Exception as e:
            logging.error(f"Error reading or transcribing audio file: {e}")
            return "file_transcription_error"
