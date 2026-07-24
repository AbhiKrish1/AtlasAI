"""
AtlasAI

Module:
    video_assembler_service.py

Responsibility:
    Assemble generated images and narration into a final
    vertical video.

Last Updated:
    Sprint 6B
"""

from __future__ import annotations

from pathlib import Path
import re

from backend.models.video import Video
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class VideoAssemblerService:
    """
    Assemble all generated assets into a finished video.

    FFmpeg integration will be added in later parts of
    Sprint 6B.
    """

    def __init__(
        self,
        output_directory: Path | str = "generated_videos",
    ) -> None:

        self._output_directory = Path(output_directory)

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def assemble(
        self,
        video: Video,
    ) -> Path:
        """
        Validate generated assets and prepare
        the output video path.

        Later parts will perform the actual
        FFmpeg assembly.
        """

        logger.info("Preparing video assembly.")

        self._validate(video)

        total_duration = self._calculate_duration(video)

        logger.info(
            "Video contains %d scene(s), total duration %.2f seconds.",
            len(video.scenes),
            total_duration,
        )

        output_path = self._build_output_path(
            video.title,
        )

        logger.info(
            "Output video will be saved to %s",
            output_path,
        )

        return output_path

    def _validate(
        self,
        video: Video,
    ) -> None:
        """
        Ensure all required assets exist.
        """

        if not video.scenes:
            raise ValueError(
                "Video contains no scenes."
            )

        if video.audio_path is None:
            raise ValueError(
                "Narration audio is missing."
            )

        for scene in video.scenes:

            if scene.image_path is None:
                raise ValueError(
                    f"Scene {scene.id} has no generated image."
                )

    def _calculate_duration(
        self,
        video: Video,
    ) -> float:
        """
        Calculate total runtime.
        """

        return sum(
            scene.duration
            for scene in video.scenes
        )

    def _build_output_path(
        self,
        title: str,
    ) -> Path:
        """
        Generate filesystem-safe output filename.
        """

        slug = self._slugify(title)

        return (
            self._output_directory
            / f"{slug}.mp4"
        )

    @staticmethod
    def _slugify(
        text: str,
    ) -> str:

        text = text.lower().strip()

        text = re.sub(
            r"[^\w\s-]",
            "",
            text,
        )

        text = re.sub(
            r"[-\s]+",
            "_",
            text,
        )

        return text