"""
Content domain models.
"""

from pydantic import BaseModel, Field


class Scene(BaseModel):
    """
    Represents a single scene in the final video.
    """

    scene_number: int = Field(..., ge=1)

    duration: int = Field(
        ...,
        gt=0,
        description="Duration of the scene in seconds."
    )

    narration: str


class ContentPlan(BaseModel):
    """
    Represents the entire content structure of a video.
    """

    topic: str

    title: str

    hook: str

    script: str

    estimated_duration: int

    scenes: list[Scene]
    