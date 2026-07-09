"""
Voice domain models.
"""

from pathlib import Path

from pydantic import BaseModel


class VoiceTrack(BaseModel):
    audio_path: Path

    subtitle_path: Path

    duration: float