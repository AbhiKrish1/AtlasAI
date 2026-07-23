"""
AtlasAI

Module:
    script_generation_service.py

Responsibility:
    Generate a structured video script from a topic using an LLM.

Last Updated:
    Sprint 5
"""

from __future__ import annotations

import json
import logging

from backend.ai.llm.base import BaseLLMClient
from backend.models.scene import Scene
from backend.models.script import Script

logger = logging.getLogger(__name__)

WORDS_PER_SECOND = 2.5
MIN_SCENE_DURATION = 2.5


class ScriptGenerationService:
    """
    Generates a structured video script using an LLM.
    """

    def __init__(self, llm: BaseLLMClient) -> None:
        self._llm = llm

    def generate_script(self, topic: str) -> Script:
        """
        Generate a script for the given topic.
        """

        logger.info("Generating script for topic: %s", topic)

        prompt = self._build_prompt(topic)

        response = self._llm.generate(prompt)

        cleaned = self._clean_response(response)

        return self._parse_response(cleaned)

    def _build_prompt(self, topic: str) -> str:
        """
        Build the LLM prompt.
        """

        return f"""
You are a professional YouTube Shorts script writer.

Generate ONLY valid JSON.

Do not include markdown.

Do not include explanations.

Return exactly five scenes.

Each scene should contain:

- id
- narration
- image_prompt

The image_prompt should be a CINEMATIC visual prompt suitable for Stable Diffusion or Flux.

Describe:

- subject
- environment
- lighting
- camera angle
- realism
- colors

Do NOT include camera settings.

Do NOT include negative prompts.

Example:

Ultra realistic NASA astrophotography of a supermassive black hole with a glowing orange accretion disk, dramatic gravitational lensing, deep space, cinematic lighting, extremely detailed, 8k, no text.

Return JSON using this schema:

{{
    "title":"...",
    "scenes":[
        {{
            "id":1,
            "narration":"...",
            "image_prompt":"..."
        }}
    ]
}}

Topic:

{topic}
"""

    def _clean_response(self, response: str) -> str:
        """
        Remove markdown code fences.
        """

        response = response.strip()

        if response.startswith("```json"):
            response = response[7:]

        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        return response.strip()

    def _estimate_duration(self, narration: str) -> float:
        """
        Estimate scene duration from narration.

        Assumes roughly 150 words/minute.
        """

        words = len(narration.split())

        duration = words / WORDS_PER_SECOND

        return max(duration, MIN_SCENE_DURATION)

    def _parse_response(self, response: str) -> Script:
        """
        Parse LLM JSON into AtlasAI models.
        """

        try:
            data = json.loads(response)

        except json.JSONDecodeError as exc:
            logger.exception("Invalid JSON returned by LLM.")
            raise ValueError("LLM returned invalid JSON.") from exc

        scenes = []

        for item in data["scenes"]:

            scenes.append(
                Scene(
                    id=item["id"],
                    narration=item["narration"],
                    image_prompt=item["image_prompt"],
                    duration=self._estimate_duration(
                        item["narration"]
                    ),
                )
            )

        return Script(
            title=data["title"],
            scenes=scenes,
        )