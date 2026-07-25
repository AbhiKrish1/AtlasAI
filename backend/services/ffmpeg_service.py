"""
AtlasAI

Module:
    ffmpeg_service.py

Responsibility:
    High-level FFmpeg operations for assembling videos.

Last Updated:
    Sprint 7.2
"""

from __future__ import annotations

from pathlib import Path

from backend.config.video import settings
from backend.models.scene import Scene
from backend.services.ffmpeg_runner import FFmpegRunner
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class FFmpegService:
    """
    High-level interface for FFmpeg operations.
    """

    def __init__(
        self,
        runner: FFmpegRunner | None = None,
        temp_directory: Path | None = None,
    ) -> None:

        self._runner = runner or FFmpegRunner()

        self._temp_directory = (
            temp_directory
            or settings.TEMP_DIRECTORY
        )

        self._temp_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def create_silent_video(
        self,
        scenes: list[Scene],
        output_path: Path,
    ) -> Path:
        """
        Convert scene images into a silent video.
        """

        logger.info(
            "Creating silent video with %d scene(s).",
            len(scenes),
        )

        clips = []

        try:

            for scene in scenes:
                clips.append(
                    self._create_scene_clip(scene)
                )

            concat_file = self._create_concat_manifest(
                clips
            )

            self._concatenate_clips(
                concat_file,
                output_path,
            )

            logger.info(
                "Silent video created successfully."
            )

            return output_path

        finally:

            self._cleanup_temp_files(
                clips
            )

    def add_audio(
        self,
        video_path: Path,
        audio_path: Path,
        output_path: Path,
    ) -> Path:
        """
        Add narration audio to a silent video.
        """

        logger.info(
            "Adding narration audio."
        )

        self._runner.run(
            [
                "-y",
                "-i",
                str(video_path),
                "-i",
                str(audio_path),
                "-c:v",
                "copy",
                "-c:a",
                "aac",
                "-shortest",
                str(output_path),
            ]
        )

        return output_path

    def burn_subtitles(
        self,
        video_path: Path,
        subtitle_path: Path,
        output_path: Path,
    ) -> Path:
        """
        Burn SRT subtitles into a video.
        """

        logger.info(
            "Burning subtitles."
        )

        escaped_path = self._escape_subtitle_path(
            subtitle_path
        )

        self._runner.run(
            [
                "-y",
                "-i",
                str(video_path),
                "-vf",
                f"subtitles='{escaped_path}'",
                "-c:a",
                "copy",
                str(output_path),
            ]
        )

        return output_path

    def _escape_subtitle_path(
        self,
        subtitle_path: Path,
    ) -> str:
        """
        Escape a subtitle path for FFmpeg's subtitles filter.

        FFmpeg expects:
        - forward slashes
        - escaped drive-letter colon
        - escaped single quotes
        """

        path = str(
            subtitle_path.resolve()
        )

        path = path.replace(
            "\\",
            "/",
        )

        if len(path) >= 2 and path[1] == ":":
            path = (
                path[0]
                + "\\:"
                + path[2:]
            )

        path = path.replace(
            "'",
            r"\'",
        )

        return path

    def _create_scene_clip(
        self,
        scene: Scene,
    ) -> Path:

        if scene.image_path is None:
            raise ValueError(
                f"Scene {scene.id} has no image."
            )

        output = (
            self._temp_directory
            / f"scene_{scene.id}.mp4"
        )

        self._runner.run(
            [
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
        )

        return output

    def _create_concat_manifest(
        self,
        clips: list[Path],
    ) -> Path:

        manifest = (
            self._temp_directory
            / "clips.txt"
        )

        with manifest.open(
            "w",
            encoding="utf-8",
        ) as file:

            for clip in clips:

                file.write(
                    f"file '{clip.resolve()}'\n"
                )

        return manifest

    def _concatenate_clips(
        self,
        manifest: Path,
        output_path: Path,
    ) -> None:

        self._runner.run(
            [
                "-y",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                str(manifest),
                "-c",
                "copy",
                str(output_path),
            ]
        )

        if manifest.exists():
            manifest.unlink()

    def _cleanup_temp_files(
        self,
        clips: list[Path],
    ) -> None:

        logger.info(
            "Cleaning temporary clips."
        )

        for clip in clips:

            try:

                if clip.exists():
                    clip.unlink()

            except Exception as exc:

                logger.warning(
                    "Unable to delete %s (%s)",
                    clip,
                    exc,
                )