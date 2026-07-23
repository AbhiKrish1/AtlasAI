"""
AtlasAI

Module:
    scene.py

Responsibility:
    Data model representing a single scene.

Last Updated:
    Sprint 5
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True)
class Scene:
    """
    Represents one scene in a generated video.
    """

    id: int

    narration: str

    image_prompt: str

    duration: float = 0.0

    image_path: Path | None = None