# File location: vidya/features/reminder_handler.py

import logging
from vidya.features.scheduler import Scheduler
import threading
import time

class ReminderHandler:
    """
    Manages reminders by using the Scheduler to run tasks at a specific time.
    """
    def __init__(self, scheduler: Scheduler, vidya_voice_synthesizer):
        self.scheduler = scheduler
        self.voice_synthesizer = vidya_voice_synthesizer
        logging.info("ReminderHandler initialized.")

    def set_reminder_at_time(self, time_str: str, message: str) -> str:
        """
        Sets a reminder to be triggered at a specific time of day (e.g., "15:30").
        """
        def reminder_task():
            self.voice_synthesizer.speak(f"Reminder: {message}")
            logging.info(f"Reminder triggered for: {message}")
            
        return self.scheduler.schedule_task_at(reminder_task, time_str)

    def set_reminder_in_minutes(self, minutes: int, message: str) -> str:
        """
        Sets a reminder to be triggered after a specific number of minutes.
        """
        seconds = minutes * 60
        def reminder_task():
            self.voice_synthesizer.speak(f"Reminder: {message}")
            logging.info(f"Reminder triggered for: {message}")
            
        return self.scheduler.schedule_task_in(reminder_task, seconds)
