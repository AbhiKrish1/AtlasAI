"""
AtlasAI

Module:
    video.py

Responsibility:
    Data model representing a generated video project.

Last Updated:
    Sprint 5
"""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.models.scene import Scene


@dataclass(slots=True)
class Video:
    """
    Represents a generated video and all of its assets.
    """

    title: str

    scenes: list[Scene] = field(default_factory=list)

    audio_path: str | None = None

    subtitle_path: str | None = None

    output_path: str | None = None