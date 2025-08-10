# File location: vidya/nlp/sentiment_analyzer_huggingface.py

import logging
from transformers import pipeline

class SentimentAnalyzerHuggingFace:
    """
    Analyzes the sentiment of text using a Hugging Face model.
    """
    def __init__(self):
        try:
            # Use a well-regarded sentiment analysis model from Hugging Face
            self.classifier = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
            logging.info("Hugging Face sentiment analysis pipeline loaded successfully.")
        except Exception as e:
            logging.error(f"Failed to load Hugging Face sentiment model: {e}")
            self.classifier = None

    def analyze(self, text: str) -> dict:
        """
        Analyzes the sentiment of a given text string.

        Args:
            text (str): The text to analyze.

        Returns:
            dict: A dictionary containing the sentiment label and score.
                  Returns an empty dict if the classifier is not available.
        """
        if not self.classifier:
            return {"label": "UNKNOWN", "score": 0.0}

        try:
            result = self.classifier(text)[0]
            logging.info(f"Analyzed sentiment for text: '{text[:30]}...' -> {result['label']} ({result['score']:.2f})")
            return result
        except Exception as e:
            logging.error(f"Error analyzing sentiment with Hugging Face: {e}")
            return {"label": "ERROR", "score": 0.0}
