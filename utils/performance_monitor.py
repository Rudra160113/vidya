# File location: vidya/utils/performance_monitor.py

import logging
import psutil
import time

class PerformanceMonitor:
    """
    Monitors system and application performance metrics.
    """
    def __init__(self):
        self.process = psutil.Process()
        logging.info("PerformanceMonitor initialized.")

    def get_cpu_usage(self) -> float:
        """Returns the current CPU usage of the system (as a percentage)."""
        try:
            return psutil.cpu_percent(interval=1)
        except Exception as e:
            logging.error(f"Failed to get CPU usage: {e}")
            return 0.0

    def get_memory_usage(self) -> dict:
        """
        Returns the memory usage of the current process (in MB) and the system (in GB).
        """
        try:
            # Process memory usage in MB
            process_memory_mb = self.process.memory_info().rss / (1024 * 1024)
            # System memory usage in GB
            system_memory = psutil.virtual_memory()
            system_memory_gb = round(system_memory.used / (1024 ** 3), 2)
            
            return {
                "process_memory_mb": process_memory_mb,
                "system_memory_gb": system_memory_gb,
                "system_memory_percent": system_memory.percent
            }
        except Exception as e:
            logging.error(f"Failed to get memory usage: {e}")
            return {}

    def get_disk_io_counters(self) -> dict:
        """
        Returns the disk I/O usage.
        """
        try:
            disk_io = psutil.disk_io_counters()
            return {
                "read_bytes": disk_io.read_bytes,
                "write_bytes": disk_io.write_bytes
            }
        except Exception as e:
            logging.error(f"Failed to get disk I/O counters: {e}")
            return {}

    def log_performance(self):
        """Logs key performance metrics."""
        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        disk = self.get_disk_io_counters()
        
        logging.info(f"Performance Metrics: CPU={cpu}%, Process_Mem={memory.get('process_memory_mb', 0)}MB, System_Mem={memory.get('system_memory_percent', 0)}%")
