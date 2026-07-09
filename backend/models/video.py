"""
Video domain models.
"""

from pathlib import Path

from pydantic import BaseModel


class VideoProject(BaseModel):
    """
    Represents the final rendered video.
    """

    output_path: Path

    duration: float

    thumbnail_path: Path | None = None