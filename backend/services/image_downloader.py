"""
AtlasAI

Module:
    image_downloader.py

Responsibility:
    Download generated images from ComfyUI.

Dependencies:
    Requests
    ComfyUI Exceptions
    Logger

Last Updated:
    Sprint 3
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import requests
from requests import RequestException

from backend.exceptions import ImageDownloadError
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ImageDownloader:
    """
    Downloads generated images from ComfyUI.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8188",
        output_dir: str | Path = "generated_images",
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )
        self.timeout = timeout

    def download_images(
        self,
        history: dict[str, Any],
    ) -> list[Path]:
        """
        Download all generated images.
        """

        images = self._extract_images(history)

        logger.info(
            "Downloading %d generated image(s).",
            len(images),
        )

        downloaded: list[Path] = []

        for image in images:
            downloaded.append(
                self._download_image(image)
            )

        logger.info(
            "Downloaded %d image(s).",
            len(downloaded),
        )

        return downloaded

    def _extract_images(
        self,
        history: dict[str, Any],
    ) -> list[dict[str, Any]]:
        """
        Extract image metadata from a workflow history entry.
        """

        images: list[dict[str, Any]] = []

        for output in history.get("outputs", {}).values():
            images.extend(
                output.get("images", [])
            )

        return images

    def _download_image(
        self,
        image: dict[str, Any],
    ) -> Path:
        """
        Download a single image.
        """

        filename = image["filename"]

        logger.info(
            "Downloading image '%s'.",
            filename,
        )

        try:
            response = requests.get(
                f"{self.base_url}/view",
                params={
                    "filename": filename,
                    "subfolder": image.get(
                        "subfolder",
                        "",
                    ),
                    "type": image.get(
                        "type",
                        "output",
                    ),
                },
                timeout=self.timeout,
            )

            response.raise_for_status()

        except RequestException as exc:
            logger.error(
                "Failed downloading image '%s'.",
                filename,
            )

            raise ImageDownloadError(
                f"Failed to download '{filename}'."
            ) from exc

        path = self.output_dir / filename

        path.write_bytes(response.content)

        logger.info(
            "Downloaded image '%s'.",
            filename,
        )

        return path