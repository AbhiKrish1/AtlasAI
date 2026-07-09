"""
Prompt domain models.
"""

from pydantic import BaseModel


class ScenePrompt(BaseModel):
    scene_number: int

    prompt: str


class PromptPlan(BaseModel):
    prompts: list[ScenePrompt]