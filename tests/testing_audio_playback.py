# File location: vidya/tests/testing_audio_playback.py

import logging
import os
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.audio.audio_playback import AudioPlayback
import wave

class TestingAudioPlayback:
    """
    A suite of tests to verify the functionality of the AudioPlayback utility.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.dummy_file = "dummy_audio.wav"
        logging.info("TestingAudioPlayback initialized.")

    def _setup_dummy_file(self):
        """Creates a dummy WAV file for testing."""
        if os.path.exists(self.dummy_file):
            os.remove(self.dummy_file)
            
        with wave.open(self.dummy_file, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(44100)
            wf.writeframes(b'dummy_data')
            
    def _cleanup_dummy_file(self):
        """Removes the dummy WAV file."""
        if os.path.exists(self.dummy_file):
            os.remove(self.dummy_file)

    @unittest.mock.patch('pyaudio.PyAudio')
    def test_playback(self, mock_pyaudio) -> bool:
        """Tests if an audio file can be played back."""
        self._setup_dummy_file()
        
        # Mock the PyAudio stream object
        mock_stream = unittest.mock.Mock()
        mock_pyaudio.return_value.open.return_value = mock_stream
        
        playback = AudioPlayback()
        
        playback.play_audio_file(self.dummy_file)
        
        # Verify that the stream write method was called
        mock_stream.write.assert_called_once()
        
        # Verify that the stream was closed
        mock_stream.stop_stream.assert_called_once()
        mock_stream.close.assert_called_once()
        
        self._cleanup_dummy_file()
        return True # The test passes if no exceptions are raised

    def run_all_tests(self):
        """Runs all audio playback tests."""
        self.test_runner.run_test("Audio Playback Test", self.test_playback)
        self.test_runner.print_summary()
