# File location: vidya/audio/audio_stream_handler.py

import logging
import pyaudio
import wave

class AudioStreamHandler:
    """
    Handles real-time audio streams from the microphone for continuous processing.
    """
    def __init__(self, chunk_size: int = 1024, format: int = pyaudio.paInt16, channels: int = 1, rate: int = 44100):
        self.chunk_size = chunk_size
        self.format = format
        self.channels = channels
        self.rate = rate
        self.pyaudio = pyaudio.PyAudio()
        self.stream = None
        logging.info("AudioStreamHandler initialized.")

    def start_stream(self):
        """Starts the audio stream from the microphone."""
        try:
            self.stream = self.pyaudio.open(format=self.format,
                                            channels=self.channels,
                                            rate=self.rate,
                                            input=True,
                                            frames_per_buffer=self.chunk_size)
            logging.info("Audio stream started.")
        except Exception as e:
            logging.error(f"Failed to start audio stream: {e}")
            self.stream = None

    def stop_stream(self):
        """Stops and closes the audio stream."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
            logging.info("Audio stream stopped.")

    def read_chunk(self) -> bytes:
        """Reads a chunk of audio data from the stream."""
        if self.stream:
            try:
                return self.stream.read(self.chunk_size)
            except IOError as e:
                logging.error(f"Error reading from audio stream: {e}")
                return b''
        return b''

    def terminate(self):
        """Terminates the PyAudio instance."""
        self.pyaudio.terminate()
        logging.info("PyAudio instance terminated.")
