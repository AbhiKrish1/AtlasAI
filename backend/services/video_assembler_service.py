"""
AtlasAI

Module:
    video_assembler_service.py

Responsibility:
    Validate a generated video and coordinate the
    assembly process.

Last Updated:
    Sprint 6C
"""

from __future__ import annotations

import re
from pathlib import Path

from backend.config.video import settings
from backend.models.video import Video
from backend.services.ffmpeg_service import FFmpegService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class VideoAssemblerService:
    """
    Coordinates video assembly.

    Validation and orchestration live here.

    FFmpeg operations are delegated to FFmpegService.
    """

    def __init__(
        self,
        ffmpeg_service: FFmpegService | None = None,
        output_directory: Path | None = None,
    ) -> None:

        self._ffmpeg = ffmpeg_service or FFmpegService()

        self._output_directory = (
            output_directory
            or settings.OUTPUT_DIRECTORY
        )

    def assemble(
        self,
        video: Video,
    ) -> Path:
        """
        Assemble a complete video with narration.
        """

        logger.info(
            "Starting video assembly."
        )

        self._validate(video)

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        output_path = self._build_output_path(
            video.title,
        )

        silent_video = (
            self._output_directory
            / f"{output_path.stem}_silent.mp4"
        )

        # Create silent video from scene images
        self._ffmpeg.create_silent_video(
            video.scenes,
            silent_video,
        )

        # Merge narration if present
        if video.audio_path:

            self._ffmpeg.add_audio(
                video_path=silent_video,
                audio_path=Path(video.audio_path),
                output_path=output_path,
            )

            if silent_video.exists():
                silent_video.unlink()

        else:
            silent_video.rename(output_path)

        logger.info(
            "Video assembly completed."
        )

        return output_path

    def _validate(
        self,
        video: Video,
    ) -> None:
        """
        Validate video assets before assembly.
        """

        if not video.scenes:
            raise ValueError(
                "Video contains no scenes."
            )

        for scene in video.scenes:

            if scene.image_path is None:
                raise ValueError(
                    f"Scene {scene.id} has no image."
                )

            if not scene.image_path.exists():
                raise FileNotFoundError(
                    scene.image_path
                )

            if scene.duration <= 0:
                raise ValueError(
                    f"Scene {scene.id} has an invalid duration."
                )

    def _build_output_path(
        self,
        title: str,
    ) -> Path:
        """
        Generate the output video path.
        """

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = (
            self._slugify(title)
            + settings.OUTPUT_EXTENSION
        )

        return self._output_directory / filename

    @staticmethod
    def _slugify(
        text: str,
    ) -> str:
        """
        Convert a title into a filesystem-safe filename.
        """

        text = text.lower().strip()

        text = re.sub(
            r"[^a-z0-9]+",
            "-",
            text,
        )

        text = re.sub(
            r"-+",
            "-",
            text,
        )

        return text.strip("-")