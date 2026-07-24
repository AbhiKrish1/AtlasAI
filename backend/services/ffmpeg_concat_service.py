"""
AtlasAI

Module:
    ffmpeg_concat_service.py

Responsibility:
    Concatenate temporary scene clips into a single silent
    video and clean up temporary assets.

Last Updated:
    Sprint 6B
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from backend.config.video import settings
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class FFmpegConcatService:
    """
    Responsible for concatenating temporary scene clips
    into a single silent video.
    """

    def __init__(
        self,
        temp_directory: Path | str | None = None,
    ) -> None:

        self._ffmpeg_binary = settings.FFMPEG_BINARY

        self._temp_directory = (
            Path(temp_directory)
            if temp_directory
            else settings.TEMP_DIRECTORY
        )

        self._temp_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def concatenate(
        self,
        clips: list[Path],
        output_path: Path,
    ) -> None:
        """
        Merge all scene clips into a single silent video.
        """

        logger.info(
            "Concatenating %d clip(s).",
            len(clips),
        )

        concat_file = self._create_concat_file(
            clips,
        )

        try:

            command = [
                self._ffmpeg_binary,
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(concat_file),
                "-c",
                "copy",
                str(output_path),
            ]

            self._run_ffmpeg(command)

        finally:

            if concat_file.exists():
                concat_file.unlink()

        logger.info(
            "Created silent video: %s",
            output_path.name,
        )

    def cleanup(
        self,
        clips: list[Path],
    ) -> None:
        """
        Delete temporary scene clips.
        """

        logger.info(
            "Cleaning temporary clips."
        )

        for clip in clips:

            try:

                if clip.exists():
                    clip.unlink()

            except Exception as exc:

                logger.warning(
                    "Failed to delete %s: %s",
                    clip,
                    exc,
                )

        logger.info(
            "Temporary cleanup complete."
        )

    def _create_concat_file(
        self,
        clips: list[Path],
    ) -> Path:
        """
        Generate an FFmpeg concat manifest.
        """

        concat_file = (
            self._temp_directory
            / "clips.txt"
        )

        with concat_file.open(
            "w",
            encoding="utf-8",
        ) as file:

            for clip in clips:

                file.write(
                    f"file '{clip.resolve()}'\n"
                )

        return concat_file

    def _run_ffmpeg(
        self,
        command: list[str],
    ) -> None:
        """
        Execute an FFmpeg command.
        """

        logger.info(
            "Running FFmpeg."
        )

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:

            logger.error(
                result.stderr,
            )

            raise RuntimeError(
                "FFmpeg command failed."
            )

        logger.info(
            "FFmpeg completed successfully."
        )