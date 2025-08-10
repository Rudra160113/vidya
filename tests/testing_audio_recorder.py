# File location: vidya/tests/testing_audio_recorder.py

import logging
import os
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.audio.audio_recorder import AudioRecorder

class TestingAudioRecorder:
    """
    A suite of tests to verify the functionality of the AudioRecorder.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.output_file = "test_recording.wav"
        logging.info("TestingAudioRecorder initialized.")
        
    def _cleanup(self):
        """Removes the test output file."""
        if os.path.exists(self.output_file):
            os.remove(self.output_file)

    @unittest.mock.patch('pyaudio.PyAudio')
    def test_record_and_save(self, mock_pyaudio) -> bool:
        """Tests if a recording can be started, a chunk recorded, and then saved to a file."""
        self._cleanup()
        
        # Mock the PyAudio stream object
        mock_stream = unittest.mock.Mock()
        mock_pyaudio.return_value.open.return_value = mock_stream
        
        recorder = AudioRecorder()
        recorder.start_recording()
        
        # Simulate recording a chunk of data
        mock_stream.read.return_value = b'test_audio_data'
        recorder.record_chunk()
        recorder.stop_recording()
        
        # Mock the wave file open call
        with unittest.mock.patch('wave.open') as mock_wave_open:
            mock_wf = unittest.mock.Mock()
            mock_wave_open.return_value = mock_wf
            
            recorder.save_recording(self.output_file)
            
            # Check if the wave file was opened and data was written
            mock_wave_open.assert_called_once_with(self.output_file, 'wb')
            mock_wf.writeframes.assert_called_once_with(b'test_audio_data')
            mock_wf.close.assert_called_once()
            
        self._cleanup()
        return True # The test passes if no exceptions are raised

    def run_all_tests(self):
        """Runs all audio recorder tests."""
        self.test_runner.run_test("Record and Save Test", self.test_record_and_save)
        self.test_runner.print_summary()
