"""
Prompt domain models.
"""

from pydantic import BaseModel


class ScenePrompt(BaseModel):
    """
    Image prompt for a single scene.
    """

    scene_number: int

    positive_prompt: str

    negative_prompt: str


class PromptPlan(BaseModel):
    """
    Collection of prompts for the whole video.
    """

    prompts: list[ScenePrompt]