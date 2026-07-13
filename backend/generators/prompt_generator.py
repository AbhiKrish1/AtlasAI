"""
Prompt Generator

Converts ContentPlan into PromptPlan.
"""

import json

from backend.models.content import ContentPlan
from backend.models.prompt import PromptPlan
from backend.services.ollama_service import OllamaService
from backend.utils.prompts import PROMPT_GENERATOR_PROMPT
from backend.utils.styles import (
    DEFAULT_NEGATIVE_STYLE,
    DEFAULT_POSITIVE_STYLE,
)


class PromptGenerator:

    def __init__(self):
        self.ollama = OllamaService()

    def generate(
        self,
        content: ContentPlan,
    ) -> PromptPlan:

        prompt = self._build_prompt(content)

        response = self.ollama.generate(prompt)

        return self._parse(response)

    def _build_prompt(
        self,
        content: ContentPlan,
    ) -> str:

        scene_text = ""

        for scene in content.scenes:
            scene_text += (
                f"Scene {scene.scene_number}: "
                f"{scene.narration}\n"
            )

        return PROMPT_GENERATOR_PROMPT.format(
            scenes=scene_text
        )

    def _parse(
        self,
        response: str,
    ) -> PromptPlan:

        data = json.loads(response)

        for prompt in data["prompts"]:

            prompt["positive_prompt"] += (
                ", "
                + DEFAULT_POSITIVE_STYLE
            )

            prompt["negative_prompt"] += (
                ", "
                + DEFAULT_NEGATIVE_STYLE
            )

        return PromptPlan(**data)