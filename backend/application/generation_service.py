"""
AtlasAI

Module:
    generation_service.py

Responsibility:
    Application layer responsible for orchestrating image generation.

Dependencies:
    ImageEngineService

Last Updated:
    Sprint 4
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.services.image_engine_service import ImageEngineService


class GenerationService:
    """
    Application service responsible for image generation.
    """

    def __init__(
        self,
        image_engine: ImageEngineService | None = None,
    ) -> None:
        self.image_engine = image_engine or ImageEngineService()

    def generate_image(
        self,
        workflow_name: str,
        parameters: dict[str, Any],
    ) -> list[Path]:
        """
        Generate images using the configured image engine.
        """

        return self.image_engine.generate_image(
            workflow_name=workflow_name,
            parameters=parameters,
        )