# File location: vidya/audio/audio_recorder.py

import logging
import pyaudio
import wave

class AudioRecorder:
    """
    A utility to record audio from the microphone.
    """
    def __init__(self, channels: int = 1, rate: int = 44100, chunk: int = 1024):
        self.channels = channels
        self.rate = rate
        self.chunk = chunk
        self.format = pyaudio.paInt16
        self.p = pyaudio.PyAudio()
        self.frames = []
        self.stream = None
        logging.info("AudioRecorder initialized.")
        
    def start_recording(self):
        """Starts the audio recording stream."""
        if self.stream and self.stream.is_active():
            logging.warning("Recording is already in progress.")
            return
            
        self.frames = []
        self.stream = self.p.open(
            format=self.format,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk
        )
        logging.info("Recording started...")

    def stop_recording(self):
        """Stops the audio recording stream."""
        if not self.stream:
            logging.warning("No recording stream to stop.")
            return
            
        self.stream.stop_stream()
        self.stream.close()
        self.stream = None
        logging.info("Recording stopped.")

    def record_chunk(self):
        """Records a single chunk of audio data."""
        if self.stream:
            data = self.stream.read(self.chunk)
            self.frames.append(data)
            
    def save_recording(self, file_path: str):
        """Saves the recorded audio data to a WAV file."""
        if not self.frames:
            logging.warning("No audio frames to save.")
            return
            
        try:
            wf = wave.open(file_path, 'wb')
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.format))
            wf.setframerate(self.rate)
            wf.writeframes(b''.join(self.frames))
            wf.close()
            logging.info(f"Recording saved to '{file_path}'.")
        except Exception as e:
            logging.error(f"Failed to save recording: {e}")
