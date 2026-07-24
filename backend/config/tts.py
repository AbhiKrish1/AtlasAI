"""
AtlasAI

Module:
    tts.py

Responsibility:
    Centralized Text-to-Speech (TTS) configuration.

Last Updated:
    Sprint 6A
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class TTSSettings:
    """
    AtlasAI Text-to-Speech configuration.
    """

    # ------------------------------------------------------------------
    # Voice
    # ------------------------------------------------------------------

    DEFAULT_VOICE: str = "en-US-GuyNeural"

    # ------------------------------------------------------------------
    # Speech Parameters
    # ------------------------------------------------------------------

    RATE: str = "+0%"
    VOLUME: str = "+0%"
    PITCH: str = "+0Hz"

    # ------------------------------------------------------------------
    # Output
    # ------------------------------------------------------------------

    OUTPUT_DIRECTORY: Path = (
        PROJECT_ROOT
        / "generated_audio"
    )

    AUDIO_FORMAT: str = "mp3"


settings = TTSSettings()