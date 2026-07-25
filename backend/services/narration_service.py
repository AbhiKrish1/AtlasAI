"""
AtlasAI

Module:
    narration_service.py

Responsibility:
    Generate narration audio from a completed script using
    Microsoft Edge-TTS.

Last Updated:
    Sprint 7.2
"""

from __future__ import annotations

import asyncio
import re
import subprocess
from pathlib import Path

import edge_tts

from backend.config.tts import settings
from backend.config.video import settings as video_settings
from backend.models.script import Script
from backend.models.video import Video
from backend.services.subtitle_service import SubtitleService
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class NarrationService:
    """
    Service responsible for converting a script into narration audio.
    """

    def __init__(self) -> None:
        self._voice = settings.DEFAULT_VOICE
        self._output_directory = settings.OUTPUT_DIRECTORY
        self._subtitle_service = SubtitleService()

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _slugify(self, text: str) -> str:
        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "_", text)
        return text

    async def _generate_audio(
        self,
        text: str,
        output_path: Path,
    ) -> None:

        communicate = edge_tts.Communicate(
            text=text,
            voice=self._voice,
            rate=settings.RATE,
            volume=settings.VOLUME,
            pitch=settings.PITCH,
        )

        await communicate.save(str(output_path))

    def generate_narration(
        self,
        script: Script,
    ) -> Path:

        logger.info("Generating narration...")

        narration_text = "\n\n".join(
            scene.narration
            for scene in script.scenes
        )

        filename = (
            f"{self._slugify(script.title)}."
            f"{settings.AUDIO_FORMAT}"
        )

        output_path = (
            self._output_directory
            / filename
        )

        asyncio.run(
            self._generate_audio(
                narration_text,
                output_path,
            )
        )

        logger.info(
            "Narration generated successfully: %s",
            output_path,
        )

        return output_path

    def _get_audio_duration(
        self,
        audio_path: Path,
    ) -> float:
        """
        Read audio duration using ffprobe.
        """

        command = [
            video_settings.FFPROBE_BINARY,
            "-v",
            "error",
            "-show_entries",
            "format=duration",
            "-of",
            "default=noprint_wrappers=1:nokey=1",
            str(audio_path),
        ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
        )

        return float(result.stdout.strip())

    def create_video(
        self,
        script: Script,
    ) -> Video:
        """
        Generate subtitles, narration, and synchronize
        scene durations with the real audio.
        """

        logger.info(
            "Creating video object for '%s'.",
            script.title,
        )

        subtitle_path = self._subtitle_service.generate_subtitles(
            script
        )

        audio_path = self.generate_narration(script)

        audio_duration = self._get_audio_duration(
            audio_path
        )

        estimated_duration = sum(
            scene.duration
            for scene in script.scenes
        )

        if estimated_duration > 0:

            scale = (
                audio_duration
                / estimated_duration
            )

            logger.info(
                "Scaling scene durations by %.3f",
                scale,
            )

            for scene in script.scenes:
                scene.duration *= scale

        logger.info(
            "Audio duration : %.2fs",
            audio_duration,
        )

        logger.info(
            "Scene duration : %.2fs",
            sum(
                scene.duration
                for scene in script.scenes
            ),
        )

        return Video(
            title=script.title,
            scenes=script.scenes,
            audio_path=str(audio_path),
            subtitle_path=str(subtitle_path),
        )