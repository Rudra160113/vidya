# File location: vidya/tests/testing_llm_processor_huggingface.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.llm.llm_processor_huggingface import LLMProcessorHuggingFace

class TestingLLMProcessorHuggingFace:
    """
    A suite of tests to verify the functionality of the LLMProcessorHuggingFace.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        logging.info("TestingLLMProcessorHuggingFace initialized.")

    @unittest.mock.patch('transformers.pipeline')
    def test_generate_response_success(self, mock_pipeline) -> bool:
        """Tests if a response is generated successfully."""
        # Mock the pipeline's return value
        mock_pipeline.return_value = unittest.mock.Mock(
            return_value=[{'generated_text': 'Hello, how can I help you today?'}]
        )
        
        processor = LLMProcessorHuggingFace()
        # Mock the tokenizer to get the correct prompt removal
        processor.tokenizer = unittest.mock.Mock()
        processor.tokenizer.eos_token_id = 1
        
        result = processor.generate_response("Hello")
        
        # We need to test the returned text, which should not include the prompt
        return "Hello" not in result and "how can I help you today?" in result

    @unittest.mock.patch('transformers.pipeline', side_effect=Exception("Model loading failed"))
    def test_loading_failure(self, mock_pipeline) -> bool:
        """Tests if the service handles a model loading failure gracefully."""
        processor = LLMProcessorHuggingFace()
        result = processor.generate_response("Test prompt")
        
        return "not configured" in result

    def run_all_tests(self):
        """Runs all Hugging Face LLM processor tests."""
        self.test_runner.run_test("Successful Response Generation", self.test_generate_response_success)
        self.test_runner.run_test("Model Loading Failure Test", self.test_loading_failure)
        self.test_runner.print_summary()
