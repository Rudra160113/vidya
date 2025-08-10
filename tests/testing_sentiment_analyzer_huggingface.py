# File location: vidya/tests/testing_sentiment_analyzer_huggingface.py

import logging
import unittest.mock
from vidya.tests.testing_framework import TestingFramework
from vidya.nlp.sentiment_analyzer_huggingface import SentimentAnalyzerHuggingFace

class TestingSentimentAnalyzerHuggingFace:
    """
    A suite of tests to verify the functionality of the SentimentAnalyzerHuggingFace.
    """
    def __init__(self):
        self.test_runner = TestingFramework()
        logging.info("TestingSentimentAnalyzerHuggingFace initialized.")

    @unittest.mock.patch('transformers.pipeline')
    def test_positive_sentiment(self, mock_pipeline) -> bool:
        """Tests if positive sentiment is correctly identified."""
        # Mock the pipeline's return value for positive sentiment
        mock_pipeline.return_value = unittest.mock.Mock(
            return_value=[{'label': 'POSITIVE', 'score': 0.999}]
        )
        
        analyzer = SentimentAnalyzerHuggingFace()
        result = analyzer.analyze("I love this project!")
        
        return result['label'] == 'POSITIVE' and result['score'] > 0.9

    @unittest.mock.patch('transformers.pipeline')
    def test_negative_sentiment(self, mock_pipeline) -> bool:
        """Tests if negative sentiment is correctly identified."""
        # Mock the pipeline's return value for negative sentiment
        mock_pipeline.return_value = unittest.mock.Mock(
            return_value=[{'label': 'NEGATIVE', 'score': 0.985}]
        )
        
        analyzer = SentimentAnalyzerHuggingFace()
        result = analyzer.analyze("This code has so many bugs.")
        
        return result['label'] == 'NEGATIVE' and result['score'] > 0.9

    @unittest.mock.patch('transformers.pipeline', side_effect=Exception("Model loading failed"))
    def test_loading_failure(self, mock_pipeline) -> bool:
        """Tests if the analyzer handles model loading failure gracefully."""
        analyzer = SentimentAnalyzerHuggingFace()
        result = analyzer.analyze("Any text")
        
        return result['label'] == 'UNKNOWN'

    def run_all_tests(self):
        """Runs all sentiment analyzer tests."""
        self.test_runner.run_test("Positive Sentiment Test", self.test_positive_sentiment)
        self.test_runner.run_test("Negative Sentiment Test", self.test_negative_sentiment)
        self.test_runner.run_test("Model Loading Failure Test", self.test_loading_failure)
        self.test_runner.print_summary()
