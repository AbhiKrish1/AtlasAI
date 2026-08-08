"""
AtlasAI

Module:
    response.py

Responsibility:
    Response schemas for the AtlasAI API.

Last Updated:
    Sprint 8
"""

from __future__ import annotations

from pydantic import BaseModel


class HealthResponse(BaseModel):
    """
    Health endpoint response.
    """

    status: str
    service: str
    version: str


class GenerateResponse(BaseModel):
    """
    Successful video generation response.
    """

    status: str
    title: str
    video: str
    subtitle: str | None = None
    audio: str | None = None