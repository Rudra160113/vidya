# File location: vidya/tests/integration_tests_huggingface.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.nlp.command_parser import CommandParser
from vidya.core.command_executor import CommandExecutor
from vidya.llm.llm_processor_huggingface import LLMProcessorHuggingFace
from vidya.nlp.sentiment_analyzer_huggingface import SentimentAnalyzerHuggingFace
from vidya.core.dependency_injector import DependencyInjector
from vidya.core.command_router import CommandRouter
from vidya.core.plugin_manager import PluginManager

class IntegrationTestsHuggingFace:
    """
    A suite of integration tests to verify the Hugging Face services work together.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        
        # Setup Dependency Injector and mock services
        self.injector = DependencyInjector()
        self.mock_llm_processor = unittest.mock.Mock(spec=LLMProcessorHuggingFace)
        self.mock_sentiment_analyzer = unittest.mock.Mock(spec=SentimentAnalyzerHuggingFace)
        self.mock_command_router = unittest.mock.Mock(spec=CommandRouter)
        self.mock_plugin_manager = unittest.mock.Mock(spec=PluginManager)

        self.injector.register(LLMProcessorHuggingFace, self.mock_llm_processor)
        self.injector.register(SentimentAnalyzerHuggingFace, self.mock_sentiment_analyzer)
        self.injector.register(CommandRouter, self.mock_command_router)
        self.injector.register('plugin_manager', self.mock_plugin_manager)

        self.parser = CommandParser()
        self.executor = CommandExecutor(self.injector)
        
        logging.info("Hugging Face Integration Test Suite initialized.")
    
    def test_sentiment_analysis_in_llm_flow(self) -> bool:
        """
        Simulates a workflow where sentiment is analyzed and used in an LLM response.
        """
        # Step 1: Simulate NLP output from a user's prompt
        user_prompt = "I'm so happy with this service!"
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
            # This is where we would call the services
            sentiment_result = self.mock_sentiment_analyzer.analyze(args['query'])
            
            # Use sentiment in the LLM prompt
            llm_prompt = f"The user is feeling {sentiment_result['label'].lower()}. Respond to their message: '{args['query']}'"
            response_text = self.mock_llm_processor.generate_response(llm_prompt)
            return response_text
        
        self.mock_command_router.get_handler.return_value = mock_chat_handler
        self.mock_sentiment_analyzer.analyze.return_value = {"label": "POSITIVE", "score": 0.99}
        self.mock_llm_processor.generate_response.return_value = "That's great to hear! I'm happy to help."
        
        # Step 4: Execute the command
        result = self.executor.execute_command(parsed_command)
        
        # Step 5: Verify the flow and the result
        self.mock_sentiment_analyzer.analyze.assert_called_once_with(user_prompt)
        self.mock_llm_processor.generate_response.assert_called_once_with("The user is feeling positive. Respond to their message: 'I'm so happy with this service!'")
        
        return result == "That's great to hear! I'm happy to help."

    def run_all_tests(self):
        """Runs all integration tests."""
        self.test_runner.run_test("Hugging Face Integration Flow Test", self.test_sentiment_analysis_in_llm_flow)
        self.test_runner.print_summary()
