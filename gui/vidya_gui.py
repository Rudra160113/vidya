# File location: vidya/gui/vidya_gui.py

import tkinter as tk
from tkinter import scrolledtext
import logging
import threading

class VidyaGUI:
    """
    A simple graphical user interface for interacting with the Vidya AI assistant.
    """
    def __init__(self, master, vidya_brain, user_id):
        self.master = master
        master.title("Vidya AI Assistant")
        
        self.vidya_brain = vidya_brain
        self.user_id = user_id

        # Chat history display area
        self.chat_history = scrolledtext.ScrolledText(master, state='disabled', wrap='word')
        self.chat_history.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Input field
        self.user_input = tk.Entry(master)
        self.user_input.pack(padx=10, pady=(0, 5), fill=tk.X)
        self.user_input.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(padx=10, pady=(0, 10))

        # Add some initial text
        self.add_message("Vidya", "Hello! How can I help you today?")
        
        logging.info("VidyaGUI initialized.")

    def add_message(self, sender: str, message: str):
        """Adds a message to the chat history display."""
        self.chat_history.config(state='normal')
        self.chat_history.insert(tk.END, f"{sender}: {message}\n\n")
        self.chat_history.config(state='disabled')
        self.chat_history.see(tk.END)

    def send_message(self, event=None):
        """Sends the user's message to the Vidya brain and displays the response."""
        user_message = self.user_input.get()
        if not user_message:
            return
            
        self.user_input.delete(0, tk.END)
        self.add_message("You", user_message)

        # Run the AI processing in a separate thread to keep the GUI responsive
        def process_and_display():
            response = self.vidya_brain.process_input(user_message, self.user_id)
            self.add_message("Vidya", response)

        threading.Thread(target=process_and_display).start()

if __name__ == '__main__':
    # This is a basic example of how to run the GUI
    # You would need to initialize VidyaBrain and SupabaseHandler
    # as you did in main.py before running this.
    print("This file is a component and should be run from a main script.")
    # Example usage:
    # from core.main import VidyaBrain, SupabaseHandler, EmailHandler
    # from vidya_gui import VidyaGUI
    # ...
    # root = tk.Tk()
    # gui_app = VidyaGUI(root, my_vidya_brain_instance, "user_001")
    # root.mainloop()
