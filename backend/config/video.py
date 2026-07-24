"""
AtlasAI

Module:
    video.py

Responsibility:
    Central configuration for video assembly.

Last Updated:
    Sprint 6B
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VideoSettings:
    """
    Configuration used by the VideoAssemblerService.
    """

    # Output directory
    OUTPUT_DIRECTORY: Path = Path("generated_videos")

    # Vertical resolution (YouTube Shorts / TikTok)
    WIDTH: int = 1080
    HEIGHT: int = 1920

    # Video
    FPS: int = 30
    VIDEO_CODEC: str = "libx264"
    PIXEL_FORMAT: str = "yuv420p"

    # Encoding
    CRF: int = 18
    PRESET: str = "medium"

    # Temporary files
    TEMP_DIRECTORY: Path = OUTPUT_DIRECTORY / "temp"

    # Final output extension
    OUTPUT_EXTENSION: str = ".mp4"

    # FFmpeg executables
    FFMPEG_BINARY: str = "ffmpeg"
    FFPROBE_BINARY: str = "ffprobe"

settings = VideoSettings()