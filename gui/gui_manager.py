# File location: vidya/gui/gui_manager.py

import tkinter as tk
import logging
from vidya.gui.vidya_gui import VidyaGUI

class GUIManager:
    """
    Manages the lifecycle and state of different GUI windows.
    """
    def __init__(self, vidya_brain, user_id):
        self.vidya_brain = vidya_brain
        self.user_id = user_id
        self.root = tk.Tk()
        self.main_gui = None
        self.windows = {}
        logging.info("GUIManager initialized.")

    def launch_main_gui(self):
        """Launches the main AI assistant window."""
        self.main_gui = VidyaGUI(self.root, self.vidya_brain, self.user_id)
        self.root.mainloop()
        
    def open_settings_window(self):
        """Opens a separate window for application settings."""
        if "settings" in self.windows and self.windows["settings"].winfo_exists():
            self.windows["settings"].lift()
            return
            
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Vidya Settings")
        
        # Placeholder content for the settings window
        tk.Label(settings_window, text="This is the settings window.").pack(padx=20, pady=20)
        
        self.windows["settings"] = settings_window
        logging.info("Settings window opened.")

    def close_all_windows(self):
        """Closes all active GUI windows."""
        for window in self.windows.values():
            if window.winfo_exists():
                window.destroy()
        if self.root.winfo_exists():
            self.root.destroy()
        logging.info("All GUI windows closed.")
