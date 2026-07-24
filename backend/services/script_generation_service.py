"""
AtlasAI

Module:
    script_generation_service.py

Responsibility:
    Generate a structured video script from a topic using an LLM.

Last Updated:
    Sprint 6D
"""

from __future__ import annotations

import json
import logging
import re

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

        last_error: Exception |None = None

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

                logger.debug("Cleaned response:\n%s", cleaned)

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

Return exactly five scenes.

Do NOT output markdown.

Do NOT output explanations.

Do NOT output comments.

Each scene MUST contain:

- id
- narration
- image_prompt

Return JSON exactly in this form:

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
        Clean common formatting issues produced by LLMs.
        """

        response = response.strip()

        # Remove UTF-8 BOM
        response = response.lstrip("\ufeff")

        # Remove markdown fences
        if response.startswith("```json"):
            response = response[7:]
        elif response.startswith("```"):
            response = response[3:]

        if response.endswith("```"):
            response = response[:-3]

        response = response.strip()

        # Replace smart quotes
        response = (
            response.replace("“", '"')
            .replace("”", '"')
            .replace("’", "'")
            .replace("‘", "'")
        )

        # Remove control characters except valid whitespace
        response = re.sub(
            r"[\x00-\x08\x0B\x0C\x0E-\x1F]",
            "",
            response,
        )

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

            logger.error(
                "JSON decode error at line %d column %d (char %d)",
                exc.lineno,
                exc.colno,
                exc.pos,
            )

            start = max(0, exc.pos - 120)
            end = min(len(response), exc.pos + 120)

            logger.error(
                "Context around error:\n%s",
                response[start:end],
            )

            raise ValueError("LLM returned invalid JSON.") from exc

        title = data.get("title")

        if not title:
            raise ValueError("Missing script title.")

        scenes_data = data.get("scenes")

        if not isinstance(scenes_data, list):
            raise ValueError("Missing scenes array.")

        if len(scenes_data) != 5:
            raise ValueError("LLM must return exactly 5 scenes.")

        scenes: list[Scene] = []

        for index, item in enumerate(scenes_data, start=1):

            narration = item.get("narration")
            image_prompt = item.get("image_prompt")

            if not narration:
                raise ValueError(
                    f"Scene {index} missing narration."
                )

            if not image_prompt:
                raise ValueError(
                    f"Scene {index} missing image_prompt."
                )

            scenes.append(
                Scene(
                    id=item.get("id", index),
                    narration=narration.strip(),
                    image_prompt=image_prompt.strip(),
                    duration=self._estimate_duration(
                        narration
                    ),
                )
            )

        return Script(
            title=title.strip(),
            scenes=scenes,
        )