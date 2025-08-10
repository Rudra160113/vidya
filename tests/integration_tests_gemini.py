# File location: vidya/tests/integration_tests_gemini.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.nlp.command_parser import CommandParser
from vidya.core.command_executor import CommandExecutor
from vidya.llm.llm_processor_gemini import LLMProcessorGemini
from vidya.core.dependency_injector import DependencyInjector
from vidya.core.command_router import CommandRouter
from vidya.core.plugin_manager import PluginManager
from vidya.security.api_key_manager import APIKeyManager
from vidya.config.configuration_manager import ConfigurationManager

class IntegrationTestsGemini:
    """
    A suite of integration tests to verify the Gemini LLM service works within the core flow.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup Dependency Injector and mock services
        self.injector = DependencyInjector()
        self.mock_api_key_manager = unittest.mock.Mock(spec=APIKeyManager)
        self.mock_config_manager = unittest.mock.Mock(spec=ConfigurationManager)
        self.mock_llm_processor = LLMProcessorGemini(self.mock_config_manager, self.mock_api_key_manager)
        self.mock_command_router = unittest.mock.Mock(spec=CommandRouter)
        self.mock_plugin_manager = unittest.mock.Mock(spec=PluginManager)

        self.injector.register(LLMProcessorGemini, self.mock_llm_processor)
        self.injector.register(CommandRouter, self.mock_command_router)
        self.injector.register('plugin_manager', self.mock_plugin_manager)

        self.parser = CommandParser()
        self.executor = CommandExecutor(self.injector)
        
        logging.info("Gemini Integration Test Suite initialized.")
    
    @unittest.mock.patch.object(LLMProcessorGemini, 'generate_response', return_value="The capital of France is Paris.")
    @unittest.mock.patch.object(APIKeyManager, 'get_key', return_value='mock-gemini-key')
    def test_gemini_in_llm_flow(self, mock_get_key, mock_generate_response) -> bool:
        """
        Simulates a workflow where a user's query is handled by the Gemini LLM.
        """
        # Step 1: Simulate NLP output for a general query
        user_prompt = "What is the capital of France?"
        nlp_output = {
            'text': user_prompt,
            'entities': {
                'command': 'chat',
                'query': user_prompt
            }
        }
        
        # Step 2: Parse the command
        parsed_command = self.parser.parse_nlp_output(nlp_output)
        
        # Step 3: Mock the command handler
        def mock_chat_handler(args):
            response_text = self.mock_llm_processor.generate_response(args['query'])
            return response_text
        
        self.mock_command_router.get_handler.return_value = mock_chat_handler
        
        # Step 4: Execute the command
        result = self.executor.execute_command(parsed_command)
        
        # Step 5: Verify the flow and the result
        self.mock_llm_processor.generate_response.assert_called_once_with(user_prompt)
        
        return result == "The capital of France is Paris."

    def run_all_tests(self):
        """Runs all integration tests."""
        self.test_runner.run_test("Gemini Integration Flow Test", self.test_gemini_in_llm_flow)
        self.test_runner.print_summary()
