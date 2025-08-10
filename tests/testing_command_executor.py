# File location: vidya/tests/testing_command_executor.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.core.command_executor import CommandExecutor
from vidya.core.command_router import CommandRouter
from vidya.core.plugin_manager import PluginManager
from vidya.core.dependency_injector import DependencyInjector

class TestingCommandExecutor:
    """
    A suite of tests to verify the functionality of the CommandExecutor.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Mock dependencies
        self.mock_command_router = unittest.mock.Mock(spec=CommandRouter)
        self.mock_plugin_manager = unittest.mock.Mock(spec=PluginManager)
        
        # Setup the mock injector
        self.injector = DependencyInjector()
        self.injector.register(CommandRouter, self.mock_command_router)
        self.injector.register('plugin_manager', self.mock_plugin_manager)
        
        self.executor = CommandExecutor(self.injector)
        logging.info("TestingCommandExecutor initialized.")

    def test_core_command_execution(self) -> bool:
        """Tests if the executor can successfully run a core command."""
        test_command = {"name": "get_weather", "args": {"location": "London"}}
        expected_result = "Weather in London is sunny."
        
        # Configure the mock router to return a handler
        mock_handler = unittest.mock.Mock(return_value=expected_result)
        self.mock_command_router.get_handler.return_value = mock_handler
        self.mock_plugin_manager.get_plugin_handler.return_value = None
        
        result = self.executor.execute_command(test_command)
        
        self.mock_command_router.get_handler.assert_called_once_with("get_weather")
        mock_handler.assert_called_once_with({"location": "London"})
        
        return result == expected_result

    def test_plugin_command_execution(self) -> bool:
        """Tests if the executor can successfully run a command from a plugin."""
        test_command = {"name": "run_plugin_action", "args": {"data": "some_value"}}
        expected_result = "Plugin action executed."
        
        # Configure the mock plugin manager to return a handler
        mock_handler = unittest.mock.Mock(return_value=expected_result)
        self.mock_command_router.get_handler.return_value = None # No core handler
        self.mock_plugin_manager.get_plugin_handler.return_value = mock_handler
        
        result = self.executor.execute_command(test_command)
        
        self.mock_plugin_manager.get_plugin_handler.assert_called_once_with("run_plugin_action")
        mock_handler.assert_called_once_with({"data": "some_value"})
        
        return result == expected_result

    def run_all_tests(self):
        """Runs all command executor tests."""
        self.test_runner.run_test("Core Command Execution Test", self.test_core_command_execution)
        self.test_runner.run_test("Plugin Command Execution Test", self.test_plugin_command_execution)
        self.test_runner.print_summary()
