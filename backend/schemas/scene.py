"""
Scene-related schemas.
"""

from pydantic import BaseModel


class Scene(BaseModel):
    """
    Represents one scene in the final video.
    """

    scene_number: int
    duration: int
    narration: str
    image_prompt: str = ""
    transition: str = "fade"


class ScenePlan(BaseModel):
    """
    Represents the complete storyboard.
    """

    topic: str
    title: str
    total_duration: int
    scenes: list[Scene]