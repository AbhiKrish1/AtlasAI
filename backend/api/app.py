"""
AtlasAI

Module:
    app.py

Responsibility:
    FastAPI application entry point.

Last Updated:
    Sprint 4
"""

from __future__ import annotations

from fastapi import FastAPI

from backend.api.routes import router

app = FastAPI(
    title="AtlasAI API",
    description="Backend API for AtlasAI image generation.",
    version="1.0.0",
)

app.include_router(router)
