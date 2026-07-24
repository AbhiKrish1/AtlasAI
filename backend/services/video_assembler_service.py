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

import re
import subprocess
from pathlib import Path

from backend.config.video import settings
from backend.models.scene import Scene
from backend.models.video import Video
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class VideoAssemblerService:
    """
    Assemble all generated assets into a finished video.

    Sprint 6B:
        ✓ Validate generated assets
        ✓ Generate temporary scene clips
        ✓ Concatenate clips into a silent video

    Future parts:
        - Add narration
        - Burn subtitles
    """

    def __init__(
        self,
        output_directory: Path | str | None = None,
    ) -> None:

        self._output_directory = (
            Path(output_directory)
            if output_directory
            else settings.OUTPUT_DIRECTORY
        )

        self._temp_directory = settings.TEMP_DIRECTORY

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._temp_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def assemble(
        self,
        video: Video,
    ) -> Path:
        """
        Assemble a generated video project.
        """

        logger.info("Preparing video assembly.")

        self._validate(video)

        total_duration = self._calculate_duration(video)

        logger.info(
            "Video contains %d scene(s), total duration %.2f seconds.",
            len(video.scenes),
            total_duration,
        )

        scene_clips: list[Path] = []

        for scene in video.scenes:

            logger.info(
                "Creating clip for Scene %d.",
                scene.id,
            )

            clip = self._create_scene_clip(scene)

            scene_clips.append(clip)

        logger.info(
            "Generated %d temporary clip(s).",
            len(scene_clips),
        )

        output_path = self._build_output_path(
            video.title,
        )

        self._concatenate_clips(
            scene_clips,
            output_path,
        )

        logger.info(
            "Silent video created successfully."
        )

        self._cleanup_temp_files(
            scene_clips,
        )

        logger.info(
            "Output video saved to %s",
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

            if not scene.image_path.exists():
                raise FileNotFoundError(
                    scene.image_path
                )

        audio = Path(video.audio_path)

        if not audio.exists():
            raise FileNotFoundError(audio)

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

    def _run_ffmpeg(
        self,
        command: list[str],
    ) -> None:
        """
        Execute an FFmpeg command.
        """

        logger.info("Running FFmpeg.")

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:

            logger.error(result.stderr)

            raise RuntimeError(
                "FFmpeg command failed."
            )

    def _create_scene_clip(
        self,
        scene: Scene,
    ) -> Path:
        """
        Convert a still image into
        a temporary MP4 clip.
        """

        output = (
            self._temp_directory
            / f"scene_{scene.id}.mp4"
        )

        command = [
            settings.FFMPEG_BINARY,
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
            "Created %s",
            output.name,
        )

        return output

    def _create_concat_file(
        self,
        clips: list[Path],
    ) -> Path:
        """
        Create an FFmpeg concat file.
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

    def _concatenate_clips(
        self,
        clips: list[Path],
        output: Path,
    ) -> None:
        """
        Merge temporary clips into
        one silent video.
        """

        concat_file = self._create_concat_file(
            clips
        )

        command = [
            settings.FFMPEG_BINARY,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(concat_file),
            "-c",
            "copy",
            str(output),
        ]

        self._run_ffmpeg(command)

    def _cleanup_temp_files(
        self,
        clips: list[Path],
    ) -> None:
        """
        Remove temporary assets.
        """

        for clip in clips:

            if clip.exists():
                clip.unlink()

        concat_file = (
            self._temp_directory
            / "clips.txt"
        )

        if concat_file.exists():
            concat_file.unlink()

    def _build_output_path(
        self,
        title: str,
    ) -> Path:
        """
        Generate filesystem-safe filename.
        """

        slug = self._slugify(title)

        return (
            self._output_directory
            / f"{slug}.{settings.OUTPUT_EXTENSION}"
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