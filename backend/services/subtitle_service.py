"""
AtlasAI

Module:
    subtitle_service.py

Responsibility:
    Generate SRT subtitle files from AtlasAI scripts.

Last Updated:
    Sprint 7A
"""

from __future__ import annotations

from pathlib import Path
import re

from backend.config.subtitles import settings
from backend.models.script import Script
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class SubtitleService:
    """
    Generates SRT subtitle files.
    """

    def __init__(self) -> None:

        self._output_directory = settings.OUTPUT_DIRECTORY

        self._output_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _slugify(
        self,
        text: str,
    ) -> str:

        text = text.lower().strip()
        text = re.sub(r"[^\w\s-]", "", text)
        text = re.sub(r"[-\s]+", "_", text)

        return text

    def _format_timestamp(
        self,
        seconds: float,
    ) -> str:

        milliseconds = int((seconds % 1) * 1000)

        total_seconds = int(seconds)

        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        secs = total_seconds % 60

        return (
            f"{hours:02}:{minutes:02}:"
            f"{secs:02},{milliseconds:03}"
        )

    def generate_subtitles(
        self,
        script: Script,
    ) -> Path:

        logger.info("Generating subtitles...")

        filename = (
            self._slugify(script.title)
            + settings.SUBTITLE_EXTENSION
        )

        output_path = (
            self._output_directory
            / filename
        )

        current_time = 0.0

        lines: list[str] = []

        for index, scene in enumerate(script.scenes, start=1):

            start = current_time
            end = start + scene.duration

            lines.append(str(index))

            lines.append(
                f"{self._format_timestamp(start)} --> "
                f"{self._format_timestamp(end)}"
            )

            lines.append(scene.narration.strip())

            lines.append("")

            current_time = end

        output_path.write_text(
            "\n".join(lines),
            encoding="utf-8",
        )

        logger.info(
            "Subtitle file generated: %s",
            output_path,
        )

        return output_path