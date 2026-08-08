"""
AtlasAI

Module:
    generate.py

Responsibility:
    API endpoint for AI video generation.

Last Updated:
    Sprint 8
"""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

from backend.api.schemas import (
    GenerateRequest,
    GenerateResponse,
)
from backend.application.generation_service import (
    GenerationService,
)
from backend.utils.logger import get_logger

logger = get_logger(__name__)

router = APIRouter(
    prefix="/generate",
    tags=["Generation"],
)

generation_service = GenerationService()


@router.post(
    "",
    response_model=GenerateResponse,
    summary="Generate AI Video",
)
def generate_video(
    request: GenerateRequest,
) -> GenerateResponse:
    """
    Generate a complete AI video from a topic.
    """

    try:
        output_path = generation_service.generate_video(
            request.topic
        )

        stem = output_path.stem

        return GenerateResponse(
            status="success",
            title=request.topic,
            video=output_path.name,
            subtitle=f"{stem}.srt",
            audio=f"{stem}.mp3",
        )

    except Exception as exc:
        logger.exception(
            "Video generation failed."
        )

        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc