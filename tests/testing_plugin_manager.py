# File location: vidya/tests/testing_plugin_manager.py

import logging
import os
import shutil
from vidya.tests.testing_framework import TestingFramework
from vidya.core.plugin_manager import PluginManager

class TestingPluginManager:
    """
    A suite of tests to verify the functionality of the PluginManager.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        self.plugin_dir = "test_plugins"
        logging.info("TestingPluginManager initialized.")

    def _setup_test_environment(self):
        """Creates a temporary directory with a dummy plugin."""
        if os.path.exists(self.plugin_dir):
            shutil.rmtree(self.plugin_dir)
        os.makedirs(self.plugin_dir)
        
        # Create a dummy plugin file
        dummy_plugin_code = """
import logging

def get_plugin_info():
    return {"name": "dummy_plugin", "version": "1.0"}

def handle_command(args):
    logging.info("Dummy command handled.")
    return "Dummy command successful."
"""
        with open(os.path.join(self.plugin_dir, "dummy_plugin.py"), 'w') as f:
            f.write(dummy_plugin_code)
            
    def _cleanup_test_environment(self):
        """Removes the temporary plugin directory."""
        if os.path.exists(self.plugin_dir):
            shutil.rmtree(self.plugin_dir)

    def test_plugin_loading(self) -> bool:
        """Tests if the plugin manager can discover and load a plugin."""
        self._setup_test_environment()
        
        manager = PluginManager(plugin_dir=self.plugin_dir)
        manager.load_plugins()
        
        self._cleanup_test_environment()
        
        # The manager should have found and loaded the dummy plugin
        return "dummy_plugin" in manager.loaded_plugins

    def run_all_tests(self):
        """Runs all plugin manager tests."""
        self.test_runner.run_test("Plugin Loading Test", self.test_plugin_loading)
        self.test_runner.print_summary()
