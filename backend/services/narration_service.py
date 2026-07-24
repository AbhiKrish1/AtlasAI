"""
AtlasAI

Module:
    narration_service.py

Responsibility:
    Generate narration audio from a completed script using
    Microsoft Edge-TTS.

Last Updated:
    Sprint 6A
"""

from __future__ import annotations

import asyncio
import re
from pathlib import Path

import edge_tts

from backend.config.tts import settings
from backend.models.script import Script
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class NarrationService:
    """
    Service responsible for converting a script into narration audio.

    This service is intentionally isolated from the rest of the
    pipeline so that future TTS providers (Azure, ElevenLabs,
    XTTS, OpenAI, etc.) can replace Edge-TTS without affecting
    VideoGenerationService.
    """

    def __init__(self) -> None:
        self._voice = settings.DEFAULT_VOICE
        self._output_directory = settings.OUTPUT_DIRECTORY

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _slugify(self, text: str) -> str:
        """
        Convert a title into a filesystem-safe filename.
        """

        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "_", text)

        return text

    async def _generate_audio(
        self,
        text: str,
        output_path: Path,
    ) -> None:
        """
        Generate narration asynchronously using Edge-TTS.
        """

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
        """
        Generate narration for a script.
        """

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

        try:
            asyncio.run(
                self._generate_audio(
                    text=narration_text,
                    output_path=output_path,
                )
            )

            logger.info(
                "Narration generated successfully: %s",
                output_path,
            )

            return output_path

        except Exception:
            logger.exception(
                "Narration generation failed."
            )
            raise