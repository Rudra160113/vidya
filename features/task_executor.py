# File location: vidya/features/task_executor.py

import logging
from vidya.features.task_automation import TaskAutomation
from vidya.features.smart_home_control import SmartHomeControl
from vidya.utils.device_admin import DeviceAdmin

class TaskExecutor:
    """
    A unified system for executing various tasks by routing commands
    to the correct handler.
    """
    def __init__(self):
        self.automation_handler = TaskAutomation()
        self.smart_home_handler = SmartHomeControl()
        self.device_admin_handler = DeviceAdmin()
        logging.info("TaskExecutor initialized with multiple handlers.")

    def execute(self, task_type: str, *args, **kwargs) -> str:
        """
        Executes a task based on its type and arguments.
        """
        task_type = task_type.lower()
        
        if task_type == "open_app":
            app_name = kwargs.get('app_name') or args[0]
            return self.automation_handler.open_application(app_name)
        
        elif task_type == "open_file":
            file_path = kwargs.get('file_path') or args[0]
            return self.automation_handler.open_file(file_path)

        elif task_type == "reboot_system":
            delay = kwargs.get('delay_seconds', 60)
            return self.device_admin_handler.reboot_system(delay)

        elif task_type == "shutdown_system":
            delay = kwargs.get('delay_seconds', 60)
            return self.device_admin_handler.shutdown_system(delay)

        elif task_type == "turn_on_light":
            light_name = kwargs.get('light_name') or args[0]
            return self.smart_home_handler.turn_on_light(light_name)

        elif task_type == "set_thermostat_temp":
            temp = kwargs.get('temp') or args[0]
            return self.smart_home_handler.set_thermostat_temp(temp)
            
        else:
            logging.warning(f"Unknown task type received: {task_type}")
            return f"I don't know how to perform the task: {task_type}."
