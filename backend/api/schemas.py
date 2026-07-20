"""
AtlasAI

Module:
    schemas.py

Responsibility:
    Pydantic request and response models for the API.

Last Updated:
    Sprint 4
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ImageGenerationRequest(BaseModel):
    """
    Request body for image generation.
    """

    workflow_name: str = Field(
        ...,
        description="Workflow package name.",
        example="txt2img",
    )

    parameters: dict[str, Any] = Field(
        default_factory=dict,
        description="Runtime parameters injected into the workflow.",
    )


class ImageGenerationResponse(BaseModel):
    """
    Response returned after successful image generation.
    """

    success: bool = True

    images: list[str]

    message: str = "Image generation completed successfully."


class HealthResponse(BaseModel):
    """
    Health check response.
    """

    status: str = "ok"

    service: str = "AtlasAI Backend"