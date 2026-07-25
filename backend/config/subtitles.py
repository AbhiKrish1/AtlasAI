"""
AtlasAI

Module:
    subtitles.py

Responsibility:
    Central configuration for subtitle generation.

Last Updated:
    Sprint 7A
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class SubtitleSettings:
    """
    Configuration used by SubtitleService.
    """

    # Output directory
    OUTPUT_DIRECTORY: Path = Path("generated_subtitles")

    # Subtitle extension
    SUBTITLE_EXTENSION: str = ".srt"


settings = SubtitleSettings()