"""
AtlasAI

Module:
    app.py

Responsibility:
    FastAPI application entry point.

Last Updated:
    Sprint 8
"""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes.download import router as download_router
from backend.api.routes.generate import router as generate_router
from backend.api.routes.health import router as health_router


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.
    """

    app = FastAPI(
        title="AtlasAI",
        description="AI-powered vertical video generation platform.",
        version="1.0.0",
    )

    #
    # CORS
    #
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    #
    # Routes
    #
    app.include_router(
        health_router,
        tags=["Health"],
    )

    app.include_router(
        generate_router,
        prefix="/api",
        tags=["Generation"],
    )

    app.include_router(
        download_router,
        prefix="/api",
        tags=["Downloads"],
    )

    return app


app = create_app()