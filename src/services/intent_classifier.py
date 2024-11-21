import asyncio

from transformers import pipeline
from typing import List

from src.app_settings import IntentClassificationSettings


# todo: we can use another model serving microservice using BentoML to serve it in scale
class IntentClassifierService:
    def __init__(self, settings: IntentClassificationSettings):
        # Initialize the zero-shot classification pipeline
        self.settings = settings
        self.classifier = pipeline(
            "zero-shot-classification", model="facebook/bart-large-mnli"
        )

    async def classify(self, text: str) -> dict:
        # Use the zero-shot classifier
        result = await self._run_pipeline(text, self.settings.candidate_labels)
        return result

    async def is_text_pertinent(self, text: str):
        classes = await self.classify(text)
        total_score = 0
        for topic_class, score in classes.items():
            total_score += score

        average_score = total_score / len(classes)
        return average_score > self.settings.threshold, classes

    async def _run_pipeline(self, text: str, candidate_labels: List[str]) -> dict:
        # Wrap the pipeline call in an async context for compatibility
        return await asyncio.to_thread(self.classifier, text, candidate_labels)
