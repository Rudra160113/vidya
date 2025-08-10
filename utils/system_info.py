# File location: vidya/utils/system_info.py

import platform
import psutil
import logging

class SystemInfo:
    """
    Gathers and provides information about the local system's hardware and OS.
    """
    def __init__(self):
        logging.info("SystemInfo initialized.")

    def get_os_info(self) -> dict:
        """Returns information about the operating system."""
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        }

    def get_cpu_info(self) -> dict:
        """Returns information about the CPU usage."""
        return {
            "physical_cores": psutil.cpu_count(logical=False),
            "total_cores": psutil.cpu_count(logical=True),
            "cpu_usage_percent": psutil.cpu_percent(interval=1, percpu=True)
        }

    def get_memory_info(self) -> dict:
        """Returns information about the system's memory."""
        memory = psutil.virtual_memory()
        return {
            "total_gb": round(memory.total / (1024 ** 3), 2),
            "available_gb": round(memory.available / (1024 ** 3), 2),
            "used_percent": memory.percent
        }

    def get_disk_info(self, path: str = '/') -> dict:
        """
        Returns information about disk usage for a specified path.
        Default path is the root directory.
        """
        try:
            disk = psutil.disk_usage(path)
            return {
                "total_gb": round(disk.total / (1024 ** 3), 2),
                "used_gb": round(disk.used / (1024 ** 3), 2),
                "free_gb": round(disk.free / (1024 ** 3), 2),
                "used_percent": disk.percent
            }
        except Exception as e:
            logging.error(f"Failed to get disk info for path {path}: {e}")
            return {"error": str(e)}

    def get_system_summary(self) -> str:
        """
        Provides a human-readable summary of the system's status.
        """
        os_info = self.get_os_info()
        cpu_info = self.get_cpu_info()
        mem_info = self.get_memory_info()
        
        summary = f"OS: {os_info['system']} {os_info['release']}\n"
        summary += f"CPU Usage: {cpu_info['cpu_usage_percent'][0]}%\n"
        summary += f"Memory Usage: {mem_info['used_percent']}% of {mem_info['total_gb']}GB\n"
        
        return summary
