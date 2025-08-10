# File location: vidya/audio/audio_playback.py

import logging
import pyaudio
import wave
import time

class AudioPlayback:
    """
    A utility to play audio files.
    """
    def __init__(self, chunk: int = 1024):
        self.chunk = chunk
        self.p = pyaudio.PyAudio()
        logging.info("AudioPlayback initialized.")

    def play_audio_file(self, file_path: str):
        """
        Plays a WAV audio file.
        """
        try:
            wf = wave.open(file_path, 'rb')
            
            stream = self.p.open(
                format=self.p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
                frames_per_buffer=self.chunk
            )
            
            data = wf.readframes(self.chunk)
            
            logging.info(f"Playing audio file: '{file_path}'...")
            
            while data:
                stream.write(data)
                data = wf.readframes(self.chunk)
            
            stream.stop_stream()
            stream.close()
            wf.close()
            
            logging.info("Audio playback finished.")
        
        except Exception as e:
            logging.error(f"Failed to play audio file '{file_path}': {e}")
