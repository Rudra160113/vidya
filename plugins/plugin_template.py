# File location: vidya/plugins/plugin_template.py

import logging

def get_plugin_info() -> dict:
    """
    Returns information about the plugin.
    
    Returns:
        dict: A dictionary containing the plugin's name, version, and a description.
    """
    return {
        "name": "template_plugin",
        "version": "0.1.0",
        "description": "A template plugin to demonstrate the plugin system."
    }

def handle_command(command_name: str, args: dict) -> str:
    """
    Handles a command dispatched to this plugin.
    
    Args:
        command_name (str): The name of the command to handle.
        args (dict): A dictionary of arguments for the command.
        
    Returns:
        str: The result of the command execution.
    """
    if command_name == "hello_world":
        name = args.get("name", "World")
        logging.info(f"Executing hello_world command for {name}.")
        return f"Hello, {name}!"
        
    # Add more command handlers as needed
    
    return f"Template plugin does not handle command '{command_name}'."
