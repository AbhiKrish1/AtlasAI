"""
AtlasAI

Module:
    routes.py

Responsibility:
    API endpoints for AtlasAI.

Last Updated:
    Sprint 4
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.application import GenerationService
from backend.api.schemas import (
    HealthResponse,
    ImageGenerationRequest,
    ImageGenerationResponse,
)

router = APIRouter()

generation_service = GenerationService()


@router.get(
    "/health",
    response_model=HealthResponse,
)
def health() -> HealthResponse:
    """
    Health check endpoint.
    """

    return HealthResponse()


@router.post(
    "/generate-image",
    response_model=ImageGenerationResponse,
)
def generate_image(
    request: ImageGenerationRequest,
) -> ImageGenerationResponse:
    """
    Generate image(s) using the selected workflow.
    """

    try:
        images = generation_service.generate_image(
            workflow_name=request.workflow_name,
            parameters=request.parameters,
        )

        return ImageGenerationResponse(
            success=True,
            images=[str(image) for image in images],
        )

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc