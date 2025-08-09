# File location: vidya/utils/auto_start.py

import os
import sys
import logging
import platform

class AutoStart:
    """
    Handles configuring the application to start automatically with the system.
    Note: Requires administrative privileges on some platforms.
    """
    def __init__(self):
        logging.info("AutoStart utility initialized.")

    def enable_auto_start(self, app_name: str = "Vidya AI", app_path: str = None) -> str:
        """
        Enables auto-start for the application.
        """
        if app_path is None:
            # Use the current script's path
            app_path = os.path.abspath(sys.argv[0])

        if platform.system() == "Windows":
            return self._enable_windows_autostart(app_name, app_path)
        elif platform.system() == "Darwin":
            return self._enable_macos_autostart(app_name, app_path)
        elif platform.system() == "Linux":
            return self._enable_linux_autostart(app_name, app_path)
        else:
            return "Auto-start is not supported on this operating system."

    def _enable_windows_autostart(self, app_name, app_path):
        """Adds a registry key for Windows auto-start."""
        try:
            import winreg as reg
            key = reg.HKEY_CURRENT_USER
            key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with reg.OpenKey(key, key_path, 0, reg.KEY_SET_VALUE) as startup_key:
                reg.SetValueEx(startup_key, app_name, 0, reg.REG_SZ, f'"{app_path}"')
            logging.info("Windows auto-start enabled successfully.")
            return "Auto-start enabled for Windows."
        except Exception as e:
            logging.error(f"Failed to enable Windows auto-start: {e}")
            return f"Failed to enable auto-start on Windows: {e}"

    def _enable_macos_autostart(self, app_name, app_path):
        """Creates a .plist file for macOS auto-start."""
        plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{app_name}.plist")
        plist_content = f"""
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{app_name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{sys.executable}</string>
        <string>{app_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
</dict>
</plist>
"""
        try:
            with open(plist_path, "w") as f:
                f.write(plist_content)
            logging.info("macOS auto-start enabled successfully.")
            return "Auto-start enabled for macOS."
        except Exception as e:
            logging.error(f"Failed to enable macOS auto-start: {e}")
            return f"Failed to enable auto-start on macOS: {e}"

    def _enable_linux_autostart(self, app_name, app_path):
        """Creates a .desktop file for Linux auto-start."""
        desktop_path = os.path.expanduser(f"~/.config/autostart/{app_name}.desktop")
        desktop_content = f"""
[Desktop Entry]
Type=Application
Exec={sys.executable} "{app_path}"
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_IN]={app_name}
Name={app_name}
Comment=Vidya AI Assistant
"""
        try:
            if not os.path.exists(os.path.dirname(desktop_path)):
                os.makedirs(os.path.dirname(desktop_path))
            with open(desktop_path, "w") as f:
                f.write(desktop_content)
            logging.info("Linux auto-start enabled successfully.")
            return "Auto-start enabled for Linux."
        except Exception as e:
            logging.error(f"Failed to enable Linux auto-start: {e}")
            return f"Failed to enable auto-start on Linux: {e}"
