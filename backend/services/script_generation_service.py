"""
AtlasAI

Module:
    script_generation_service.py

Responsibility:
    Generate a structured video script from a topic using an LLM.

Last Updated:
    Sprint 6A
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
MAX_RETRIES = 3


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

        last_error: Exception | None = None

        for attempt in range(1, MAX_RETRIES + 1):

            logger.info(
                "Script generation attempt %d/%d",
                attempt,
                MAX_RETRIES,
            )

            response = self._llm.generate(prompt)

            cleaned = self._clean_response(response)

            try:
                return self._parse_response(cleaned)

            except ValueError as exc:

                last_error = exc

                logger.warning(
                    "Invalid JSON received from LLM on attempt %d.",
                    attempt,
                )

                logger.debug("LLM Response:\n%s", cleaned)

        raise RuntimeError(
            "Failed to generate a valid script after "
            f"{MAX_RETRIES} attempts."
        ) from last_error

    def _build_prompt(self, topic: str) -> str:
        """
        Build the LLM prompt.
        """

        return f"""
You are a professional YouTube Shorts script writer.

Return ONLY valid RFC8259 JSON.

Do not include markdown.

Do not include explanations.

Do not include comments.

Do not include trailing commas.

Return exactly five scenes.

Every scene MUST contain ALL of these keys:

- id
- narration
- image_prompt

Do not omit any keys.

The image_prompt should be a cinematic visual prompt suitable for
Stable Diffusion or Flux.

Describe:

- subject
- environment
- lighting
- camera angle
- realism
- colors

Do NOT include camera settings.

Do NOT include negative prompts.

Return JSON using EXACTLY this schema:

{{
    "title": "...",
    "scenes": [
        {{
            "id": 1,
            "narration": "...",
            "image_prompt": "..."
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

            logger.error("Invalid JSON returned by LLM.")
            logger.debug("LLM Response:\n%s", response)

            raise ValueError("LLM returned invalid JSON.") from exc

        title = data.get("title")

        if not title:
            raise ValueError("Missing script title.")

        scenes_data = data.get("scenes")

        if not isinstance(scenes_data, list):
            raise ValueError("Missing scenes array.")

        scenes: list[Scene] = []

        for index, item in enumerate(scenes_data, start=1):

            narration = item.get("narration")
            image_prompt = item.get("image_prompt")

            if narration is None:
                raise ValueError(
                    f"Scene {index} missing narration."
                )

            if image_prompt is None:
                raise ValueError(
                    f"Scene {index} missing image_prompt."
                )

            scenes.append(
                Scene(
                    id=item.get("id", index),
                    narration=narration,
                    image_prompt=image_prompt,
                    duration=self._estimate_duration(
                        narration
                    ),
                )
            )

        return Script(
            title=title,
            scenes=scenes,
        )