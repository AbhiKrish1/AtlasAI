"""
Content Generator

Generates the complete content plan for a video.
"""

import json

from backend.models.content import ContentPlan
from backend.services.ollama_service import OllamaService
from backend.utils.prompts import CONTENT_PROMPT


class ContentGenerator:
    """
    Generates a complete ContentPlan using Ollama.
    """

    def __init__(self):
        self.ollama = OllamaService()

    def generate(self, topic: str) -> ContentPlan:
        """
        Generate a complete content plan.
        """

        self._validate(topic)

        prompt = self._build_prompt(topic)

        response = self._call_model(prompt)

        return self._parse_response(response, topic)

    def _validate(self, topic: str) -> None:
        if not topic.strip():
            raise ValueError("Topic cannot be empty.")

    def _build_prompt(self, topic: str) -> str:
        return CONTENT_PROMPT.format(topic=topic)

    def _call_model(self, prompt: str) -> str:
        return self.ollama.generate(prompt)

    def _parse_response(
        self,
        response: str,
        topic: str,
    ) -> ContentPlan:

        data = json.loads(response)

        data["topic"] = topic

        return ContentPlan(**data)