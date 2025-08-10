# File location: vidya/core/command_executor.py

import logging
from vidya.core.dependency_injector import DependencyInjector
from vidya.core.command_router import CommandRouter

class CommandExecutor:
    """
    Executes a parsed command by routing it to the appropriate service or plugin.
    """
    def __init__(self, dependency_injector: DependencyInjector):
        self.injector = dependency_injector
        self.command_router = self.injector.get(CommandRouter)
        self.plugin_manager = self.injector.get('plugin_manager')
        logging.info("CommandExecutor initialized.")

    def execute_command(self, command: dict) -> str:
        """
        Executes a command based on its type and parameters.
        
        Args:
            command (dict): A dictionary containing the command and its arguments.
            
        Returns:
            str: The result or status message of the executed command.
        """
        command_name = command.get('name')
        if not command_name:
            return "Error: Command name is missing."
            
        logging.info(f"Executing command: {command_name} with args: {command.get('args', {})}")
        
        # Try to find a core command handler first
        handler = self.command_router.get_handler(command_name)
        if handler:
            return handler(command.get('args', {}))
            
        # If not a core command, check for a plugin handler
        if self.plugin_manager:
            plugin_handler = self.plugin_manager.get_plugin_handler(command_name)
            if plugin_handler:
                return plugin_handler(command.get('args', {}))
                
        logging.warning(f"No handler found for command: {command_name}")
        return f"I'm sorry, I don't know how to execute the command '{command_name}'."
