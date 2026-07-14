"""
AtlasAI

Module:
    settings.py

Responsibility:
    Centralized application configuration.

Last Updated:
    Sprint 4
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    """
    AtlasAI application settings.
    """

    # ------------------------------------------------------------------
    # ComfyUI
    # ------------------------------------------------------------------

    COMFYUI_URL: str = "http://127.0.0.1:8188"
    COMFYUI_TIMEOUT: int = 30

    # ------------------------------------------------------------------
    # Workflows
    # ------------------------------------------------------------------

    WORKFLOW_DIRECTORY: Path = (
        PROJECT_ROOT
        / "resources"
        / "workflows"
    )

    DEFAULT_WORKFLOW: str = "txt2img"

    # ------------------------------------------------------------------
    # Generated Images
    # ------------------------------------------------------------------

    OUTPUT_DIRECTORY: Path = (
        PROJECT_ROOT
        / "generated_images"
    )

    # ------------------------------------------------------------------
    # Logging
    # ------------------------------------------------------------------

    LOG_LEVEL: str = "INFO"


settings = Settings()