# File location: vidya/audio/speech_recognition.py

import logging
from vidya.audio.voice_listener import VoiceListener
from vidya.audio.voice_to_text import VoiceToText

class SpeechRecognition:
    """
    Orchestrates the entire speech recognition process, from listening
    for audio to transcribing it into text.
    """
    def __init__(self):
        self.listener = VoiceListener()
        self.transcriber = VoiceToText()
        logging.info("SpeechRecognition module initialized.")

    def get_command_from_mic(self) -> str:
        """
        Listens for audio from the microphone and returns the transcribed text.
        """
        logging.info("Awaiting voice command...")
        audio_data = self.listener.listen_for_audio()
        
        if audio_data:
            transcribed_text = self.transcriber.transcribe_audio(audio_data)
            return transcribed_text
        else:
            return ""

    def get_command_from_file(self, audio_file_path: str) -> str:
        """
        Transcribes an audio file into text.
        """
        logging.info(f"Transcribing audio from file: {audio_file_path}")
        transcribed_text = self.transcriber.transcribe_audio_from_file(audio_file_path)
        return transcribed_text
