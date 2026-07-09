"""
Image domain models.
"""

from pathlib import Path

from pydantic import BaseModel


class SceneImage(BaseModel):
    scene_number: int

    image_path: Path


class ImageSet(BaseModel):
    images: list[SceneImage]