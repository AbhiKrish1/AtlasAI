"""
AtlasAI

Module:
    ffmpeg_service.py

Responsibility:
    Centralized service for all FFmpeg operations.

    Sprint 6B Part 1:
        - Generate temporary scene clips
        - Execute FFmpeg commands

Last Updated:
    Sprint 6B
"""

from __future__ import annotations

import subprocess
from pathlib import Path

from backend.config.video import settings
from backend.models.scene import Scene
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class FFmpegService:
    """
    Encapsulates all FFmpeg operations used by AtlasAI.

    Public API:
        - create_scene_clips()

    Future additions:
        - concatenate_clips()
        - add_audio()
        - burn_subtitles()
        - cleanup()
    """

    def __init__(
        self,
        temp_directory: Path | str | None = None,
    ) -> None:
        """
        Initialize the FFmpeg service.
        """

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

    def create_scene_clips(
        self,
        scenes: list[Scene],
    ) -> list[Path]:
        """
        Generate one temporary MP4 clip for each scene.

        Returns
        -------
        list[Path]
            Paths to all generated clips.
        """

        logger.info(
            "Generating %d temporary scene clip(s).",
            len(scenes),
        )

        clips: list[Path] = []

        for scene in scenes:

            logger.info(
                "Generating clip for Scene %d.",
                scene.id,
            )

            clip = self._create_scene_clip(
                scene,
            )

            clips.append(clip)

        logger.info(
            "Successfully generated %d clip(s).",
            len(clips),
        )

        return clips

    def _create_scene_clip(
        self,
        scene: Scene,
    ) -> Path:
        """
        Convert a still image into a temporary MP4 clip.
        """

        output = (
            self._temp_directory
            / f"scene_{scene.id}.mp4"
        )

        command = [
            self._ffmpeg_binary,
            "-y",
            "-loop",
            "1",
            "-i",
            str(scene.image_path),
            "-t",
            str(scene.duration),
            "-r",
            str(settings.FPS),
            "-vf",
            (
                f"scale="
                f"{settings.WIDTH}:{settings.HEIGHT}"
            ),
            "-c:v",
            settings.VIDEO_CODEC,
            "-pix_fmt",
            settings.PIXEL_FORMAT,
            "-preset",
            settings.PRESET,
            "-crf",
            str(settings.CRF),
            str(output),
        ]

        self._run_ffmpeg(command)

        logger.info(
            "Created clip %s",
            output.name,
        )

        return output

    def _run_ffmpeg(
        self,
        command: list[str],
    ) -> None:
        """
        Execute an FFmpeg command.

        Raises
        ------
        RuntimeError
            If FFmpeg returns a non-zero exit code.
        """

        logger.info(
            "Running FFmpeg command."
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
            "FFmpeg completed successfully."
        )