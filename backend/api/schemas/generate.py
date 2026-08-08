"""
AtlasAI

Module:
    generate.py

Responsibility:
    Request schema for video generation.

Last Updated:
    Sprint 8
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class GenerateRequest(BaseModel):
    """
    Request body for generating a video.
    """

    topic: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Topic to generate a video about.",
        examples=["Top 5 Facts About Black Holes"],
    )