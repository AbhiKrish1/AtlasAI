"""
AtlasAI

Module:
    health.py

Responsibility:
    Health check endpoints.

Last Updated:
    Sprint 8
"""

from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get(
    "/health",
    summary="Health Check",
    response_description="API health status",
)
def health_check() -> dict[str, str]:
    """
    Verify that the AtlasAI API is running.
    """

    return {
        "status": "healthy",
        "service": "AtlasAI",
        "version": "1.0.0",
    }