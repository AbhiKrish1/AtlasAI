"""
AtlasAI

Module:
    download.py

Responsibility:
    Download generated AtlasAI assets.

Last Updated:
    Sprint 8
"""

from __future__ import annotations

from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from backend.config.video import settings as video_settings
from backend.config.subtitles import settings as subtitle_settings
from backend.config.tts import settings as tts_settings

router = APIRouter(
    prefix="/download",
    tags=["Downloads"],
)

DIRECTORIES = {
    "video": video_settings.OUTPUT_DIRECTORY,
    "subtitle": subtitle_settings.OUTPUT_DIRECTORY,
    "audio": tts_settings.OUTPUT_DIRECTORY,
}


@router.get("/{asset_type}/{filename}")
def download_asset(
    asset_type: str,
    filename: str,
) -> FileResponse:
    """
    Download a generated AtlasAI asset.

    Supported asset types:

    - video
    - subtitle
    - audio
    """

    asset_type = asset_type.lower()

    if asset_type not in DIRECTORIES:
        raise HTTPException(
            status_code=404,
            detail=f"Unsupported asset type '{asset_type}'.",
        )

    directory: Path = DIRECTORIES[asset_type]
    file_path = directory / filename

    if not file_path.exists():
        raise HTTPException(
            status_code=404,
            detail=f"{asset_type.capitalize()} file not found.",
        )

    return FileResponse(
        path=file_path,
        filename=file_path.name,
        media_type="application/octet-stream",
    )