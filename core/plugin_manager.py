# File location: vidya/core/plugin_manager.py

import importlib
import logging
import os
import sys

class PluginManager:
    """
    Manages the loading, activation, and deactivation of plugins.
    """
    def __init__(self, plugins_dir: str = 'vidya/plugins'):
        self.plugins_dir = plugins_dir
        self.plugins = {}
        logging.info("PluginManager initialized.")

    def load_plugins(self):
        """
        Discovers and loads all plugins from the plugins directory.
        """
        # Add the plugins directory to the Python path
        sys.path.append(os.path.abspath(os.path.dirname(self.plugins_dir)))
        
        if not os.path.exists(self.plugins_dir):
            logging.warning(f"Plugins directory '{self.plugins_dir}' not found. No plugins will be loaded.")
            return
            
        logging.info(f"Scanning for plugins in '{self.plugins_dir}'...")
        
        for plugin_name in os.listdir(self.plugins_dir):
            if plugin_name.endswith('.py') and not plugin_name.startswith('__'):
                module_name = plugin_name[:-3]
                try:
                    module = importlib.import_module(f"vidya.plugins.{module_name}")
                    if hasattr(module, 'setup'):
                        self.plugins[module_name] = module.setup()
                        logging.info(f"Plugin '{module_name}' loaded successfully.")
                    else:
                        logging.warning(f"Plugin '{module_name}' is missing a 'setup' function.")
                except Exception as e:
                    logging.error(f"Failed to load plugin '{module_name}': {e}")

    def get_plugin(self, plugin_name: str):
        """
        Retrieves an instance of a loaded plugin.
        """
        return self.plugins.get(plugin_name)
