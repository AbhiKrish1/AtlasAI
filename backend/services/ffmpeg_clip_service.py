"""
AtlasAI

Module:
    ffmpeg_clip_service.py

Responsibility:
    Generate temporary MP4 clips from scene images using FFmpeg.

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


class FFmpegClipService:
    """
    Responsible for converting scene images into
    temporary MP4 clips.
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

    def create_scene_clips(
        self,
        scenes: list[Scene],
    ) -> list[Path]:
        """
        Generate one MP4 clip for every scene.
        """

        logger.info(
            "Generating %d scene clip(s).",
            len(scenes),
        )

        clips: list[Path] = []

        for scene in scenes:

            clips.append(
                self._create_scene_clip(scene)
            )

        logger.info(
            "Generated %d scene clip(s).",
            len(clips),
        )

        return clips

    def _create_scene_clip(
        self,
        scene: Scene,
    ) -> Path:
        """
        Convert one still image into an MP4 clip.
        """

        if scene.image_path is None:
            raise ValueError(
                f"Scene {scene.id} has no image."
            )

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