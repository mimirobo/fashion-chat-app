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

    async def is_text_pertinent(self, text: str, reference_labels: dict):
        classes = await self.classify(text)
        weighted_score_sum = 0
        total_weight = 0

        # Calculate the weighted sum and total weight
        for topic_class, score in classes.items():
            weight = reference_labels.get(
                topic_class, 1
            )  # Default weight is 1 if not found
            weighted_score_sum += score * weight
            total_weight += weight

        # Calculate the weighted average score
        weighted_average_score = (
            weighted_score_sum / total_weight if total_weight != 0 else 0
        )

        return weighted_average_score > self.settings.threshold, classes

    async def _run_pipeline(self, text: str, candidate_labels: List[str]) -> dict:
        # Wrap the pipeline call in an async context for compatibility
        return await asyncio.to_thread(self.classifier, text, candidate_labels)
