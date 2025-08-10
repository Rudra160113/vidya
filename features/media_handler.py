# File location: vidya/features/media_handler.py

import logging
import subprocess
import os

class MediaHandler:
    """
    Handles playing and managing media files (audio, video).
    """
    def __init__(self):
        logging.info("MediaHandler initialized.")

    def play_audio(self, audio_file_path: str) -> str:
        """
        Plays an audio file using the system's default player.
        """
        if not os.path.exists(audio_file_path):
            logging.error(f"Audio file not found: {audio_file_path}")
            return "Audio file not found."
            
        try:
            # Using subprocess to open the file with the default program
            subprocess.Popen([audio_file_path], shell=True)
            logging.info(f"Playing audio file: {audio_file_path}")
            return "Playing the audio."
        except Exception as e:
            logging.error(f"Failed to play audio file: {e}")
            return "An error occurred while trying to play the audio."

    def play_video(self, video_file_path: str) -> str:
        """
        Plays a video file using the system's default player.
        """
        if not os.path.exists(video_file_path):
            logging.error(f"Video file not found: {video_file_path}")
            return "Video file not found."
            
        try:
            subprocess.Popen([video_file_path], shell=True)
            logging.info(f"Playing video file: {video_file_path}")
            return "Playing the video."
        except Exception as e:
            logging.error(f"Failed to play video file: {e}")
            return "An error occurred while trying to play the video."
