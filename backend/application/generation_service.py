"""
AtlasAI

Module:
    generation_service.py

Responsibility:
    Application layer responsible for orchestrating the
    complete AI video generation pipeline.

Dependencies:
    OllamaClient
    ScriptGenerationService
    ImageEngineService
    NarrationService
    VideoAssemblerService

Last Updated:
    Sprint 6C
"""

from __future__ import annotations

from pathlib import Path

from backend.ai.llm.ollama_client import OllamaClient
from backend.services.image_engine_service import (
    ImageEngineService,
)
from backend.services.narration_service import (
    NarrationService,
)
from backend.services.script_generation_service import (
    ScriptGenerationService,
)
from backend.services.video_assembler_service import (
    VideoAssemblerService,
)
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class GenerationService:
    """
    High-level application service responsible for
    orchestrating the complete AtlasAI pipeline.
    """

    def __init__(
        self,
        llm: OllamaClient | None = None,
        script_service: ScriptGenerationService | None = None,
        image_service: ImageEngineService | None = None,
        narration_service: NarrationService | None = None,
        video_assembler: VideoAssemblerService | None = None,
    ) -> None:

        llm = llm or OllamaClient()

        self.script_service = (
            script_service
            or ScriptGenerationService(llm)
        )

        self.image_service = (
            image_service
            or ImageEngineService()
        )

        self.narration_service = (
            narration_service
            or NarrationService()
        )

        self.video_assembler = (
            video_assembler
            or VideoAssemblerService()
        )

    def generate_video(
        self,
        topic: str,
    ) -> Path:
        """
        Generate a complete AI video from a topic.

        Parameters
        ----------
        topic
            Topic to generate.

        Returns
        -------
        Path
            Path to the generated MP4.
        """

        logger.info(
            "Starting video generation for '%s'.",
            topic,
        )

        # Step 1: Generate script
        script = self.script_service.generate_script(
            topic
        )

        # Step 2: Generate images
        script = (
            self.image_service
            .generate_images_for_script(script)
        )

        # Step 3: Generate narration and Video model
        video = (
            self.narration_service
            .create_video(script)
        )

        # Step 4: Assemble final video
        output_path = (
            self.video_assembler
            .assemble(video)
        )

        logger.info(
            "Video generation completed successfully."
        )

        return output_path