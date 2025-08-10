# File location: vidya/tests/testing_plugin_suite.py

import logging
from vidya.tests.testing_framework import TestingFramework
from vidya.core.plugin_manager import PluginManager
import os
import shutil

# Placeholder for a mock plugin file
MOCK_PLUGIN_CODE = """
# File location: vidya/plugins/mock_plugin.py

def register_plugin():
    return MockPlugin()

class MockPlugin:
    def __init__(self):
        self.name = "MockPlugin"
        self.is_active = False

    def activate(self):
        self.is_active = True
    
    def get_info(self):
        return f"Hello from {self.name}!"
"""

class TestingPluginSuite:
    """
    A suite of tests to verify the functionality of the PluginManager.
    """
    def __init__(self, plugin_dir: str = 'vidya/plugins'):
        self.plugin_dir = plugin_dir
        self._setup_mock_environment()
        self.plugin_manager = PluginManager(plugin_dir=self.plugin_dir)
        self.test_runner = TestingFramework()
        logging.info("TestingPluginSuite initialized.")

    def _setup_mock_environment(self):
        """Creates a temporary directory and a mock plugin file for testing."""
        if os.path.exists(self.plugin_dir):
            shutil.rmtree(self.plugin_dir)
        os.makedirs(self.plugin_dir)
        with open(os.path.join(self.plugin_dir, 'mock_plugin.py'), 'w') as f:
            f.write(MOCK_PLUGIN_CODE)
        
    def test_plugin_loading(self) -> bool:
        """Tests if the plugin manager can discover and load a plugin."""
        self.plugin_manager.load_plugins()
        return "mock_plugin" in self.plugin_manager.plugins

    def test_plugin_enabling(self) -> bool:
        """Tests if a loaded plugin can be enabled and its methods can be called."""
        self.plugin_manager.load_plugins()
        self.plugin_manager.enable_plugin("mock_plugin")
        
        enabled_plugins = self.plugin_manager.get_enabled_plugins()
        if not enabled_plugins:
            return False
            
        plugin_instance = enabled_plugins[0]
        plugin_instance.activate()
        
        return plugin_instance.is_active and plugin_instance.get_info() == "Hello from MockPlugin!"

    def run_all_tests(self):
        """Runs all plugin-related tests in the suite."""
        self.test_runner.run_test("Plugin Loading Test", self.test_plugin_loading)
        self.test_runner.run_test("Plugin Enabling Test", self.test_plugin_enabling)
        self.test_runner.print_summary()
