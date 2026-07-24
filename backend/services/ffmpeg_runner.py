"""
AtlasAI

Module:
    ffmpeg_runner.py

Responsibility:
    Execute FFmpeg commands with consistent logging and
    error handling.

Last Updated:
    Sprint 6B
"""

from __future__ import annotations

import subprocess

from backend.config.video import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class FFmpegRunner:
    """
    Executes FFmpeg commands.
    """

    def __init__(
        self,
        ffmpeg_binary: str | None = None,
    ) -> None:
        self._ffmpeg_binary = (
            ffmpeg_binary
            or settings.FFMPEG_BINARY
        )

    @property
    def ffmpeg_binary(self) -> str:
        """
        Return the configured FFmpeg executable.
        """
        return self._ffmpeg_binary

    def run(
        self,
        arguments: list[str],
    ) -> None:
        """
        Execute an FFmpeg command.

        Parameters
        ----------
        arguments:
            Command-line arguments excluding the FFmpeg
            executable.
        """

        command = [
            self._ffmpeg_binary,
            *arguments,
        ]

        logger.info(
            "Executing FFmpeg command."
        )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            logger.error(
                "FFmpeg failed:\n%s",
                result.stderr,
            )

            raise RuntimeError(
                "FFmpeg command failed."
            )

        logger.info(
            "FFmpeg command completed successfully."
        )