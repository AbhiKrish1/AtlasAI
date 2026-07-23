"""
AtlasAI

Module:
    script.py

Responsibility:
    Data model representing an AI-generated video script.

Last Updated:
    Sprint 5
"""

from __future__ import annotations

from dataclasses import dataclass, field

from backend.models.scene import Scene


@dataclass(slots=True)
class Script:
    """
    Represents a complete video script generated
    from a user topic.
    """

    title: str

    scenes: list[Scene] = field(default_factory=list)