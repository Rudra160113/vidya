# File location: vidya/utils/device_admin.py

import os
import subprocess
import platform
import logging

class DeviceAdmin:
    """
    Manages system-level administrative tasks like rebooting, shutting down,
    and logging out the device.
    """
    def __init__(self):
        logging.info("DeviceAdmin initialized.")

    def reboot_system(self, delay_seconds: int = 60) -> str:
        """
        Reboots the system after a specified delay.
        Warning: This function will forcefully restart the computer.
        """
        logging.warning(f"Reboot command received. Rebooting in {delay_seconds} seconds.")
        command = ""
        system = platform.system()
        
        if system == "Windows":
            command = f"shutdown /r /t {delay_seconds}"
        elif system == "Darwin" or system == "Linux":
            command = f"sudo shutdown -r +{delay_seconds // 60}"
            
        if command:
            try:
                # Execute the command with a sub-process
                subprocess.run(command, shell=True, check=True)
                return f"Rebooting the system in {delay_seconds} seconds. All unsaved work will be lost."
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to execute reboot command: {e}")
                return "Failed to reboot. Please check if you have the necessary administrative privileges."
            except Exception as e:
                logging.error(f"An unexpected error occurred during reboot: {e}")
                return "An error occurred. I could not initiate a reboot."
        else:
            return "System reboot is not supported on this operating system."

    def shutdown_system(self, delay_seconds: int = 60) -> str:
        """
        Shuts down the system after a specified delay.
        """
        logging.warning(f"Shutdown command received. Shutting down in {delay_seconds} seconds.")
        command = ""
        system = platform.system()

        if system == "Windows":
            command = f"shutdown /s /t {delay_seconds}"
        elif system == "Darwin" or system == "Linux":
            command = f"sudo shutdown -h +{delay_seconds // 60}"
            
        if command:
            try:
                subprocess.run(command, shell=True, check=True)
                return f"Shutting down the system in {delay_seconds} seconds."
            except subprocess.CalledProcessError as e:
                logging.error(f"Failed to execute shutdown command: {e}")
                return "Failed to shut down. Please check administrative privileges."
            except Exception as e:
                logging.error(f"An unexpected error occurred during shutdown: {e}")
                return "An error occurred. I could not initiate a shutdown."
        else:
            return "System shutdown is not supported on this operating system."
