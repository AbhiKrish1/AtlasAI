"""
ScenePlanner

Converts a script into a structured scene plan.
"""

import json

from backend.schemas.scene import ScenePlan
from backend.schemas.script import ScriptResponse
from backend.services.ollama_service import OllamaService
from backend.utils.prompts import SCENE_PROMPT


class ScenePlanner:
    """
    Plans scenes from a generated script.
    """

    def __init__(self):
        self.ollama = OllamaService()

    def generate(self, script: ScriptResponse) -> ScenePlan:
        self._validate(script)

        prompt = self._build_prompt(script)

        raw_response = self.ollama.generate(prompt)

        return self._parse_response(
            raw_response,
            script,
        )

    def _validate(self, script: ScriptResponse) -> None:
        if not script.script.strip():
            raise ValueError("Script cannot be empty.")

    def _build_prompt(self, script: ScriptResponse) -> str:
        return SCENE_PROMPT.format(
            script=script.script
        )

    def _parse_response(
        self,
        response: str,
        script: ScriptResponse,
    ) -> ScenePlan:

        data = json.loads(response)

        data["topic"] = script.title
        data["title"] = script.title
        data["total_duration"] = script.estimated_duration

        return ScenePlan(**data)