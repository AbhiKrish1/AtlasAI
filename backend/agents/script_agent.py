"""
ScriptAgent

Responsible for generating structured YouTube Shorts scripts.
"""

import json

from backend.schemas.script import ScriptResponse
from backend.services.ollama_service import OllamaService
from backend.utils.prompts import SCRIPT_PROMPT


class ScriptAgent:
    """
    Generates scripts using the configured LLM.
    """

    def __init__(self):
        self.ollama = OllamaService()

    def generate(self, topic: str) -> ScriptResponse:
        """
        Generate a structured script from a topic.
        """

        self._validate_topic(topic)

        prompt = self._build_prompt(topic)

        raw_response = self.ollama.generate(prompt)

        return self._parse_response(raw_response)

    def _validate_topic(self, topic: str) -> None:
        """
        Validate user input.
        """

        if not topic.strip():
            raise ValueError("Topic cannot be empty.")

    def _build_prompt(self, topic: str) -> str:
        """
        Insert the topic into the prompt template.
        """

        return SCRIPT_PROMPT.format(topic=topic)

    def _parse_response(self, response: str) -> ScriptResponse:
        """
        Convert Ollama JSON into a ScriptResponse.
        """

        data = json.loads(response)

        return ScriptResponse(**data)