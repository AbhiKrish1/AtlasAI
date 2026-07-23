"""
AtlasAI

Module:
    video_generation_service.py

Responsibility:
    Orchestrates the complete AI video generation pipeline.

Last Updated:
    Sprint 5
"""

from __future__ import annotations

import logging
import random
from backend.models.video import Video
from backend.services.image_engine_service import ImageEngineService
from backend.services.script_generation_service import (
    ScriptGenerationService,
)

logger = logging.getLogger(__name__)


class VideoGenerationService:
    """
    Coordinates the complete video generation pipeline.
    """

    def __init__(
        self,
        script_service: ScriptGenerationService,
        image_service: ImageEngineService | None = None,
    ) -> None:
        self._script_service = script_service
        self._image_service = image_service or ImageEngineService()

    def generate_video(self, topic: str) -> Video:
        """
        Generate a video project from a topic.

        Current pipeline:

        Topic
            ↓
        Script Generation
            ↓
        Image Generation
        """

        logger.info("Starting video generation.")

        script = self._generate_script(topic)

        video = Video(
            title=script.title,
            scenes=script.scenes,
        )

        self._generate_images(video)

        logger.info(
            "Video project generated successfully."
        )

        return video

    def _generate_script(self, topic: str):
        """
        Generate the video script.
        """

        logger.info("Generating script.")

        return self._script_service.generate_script(topic)

    def _generate_images(self, video: Video) -> None:
        """
        Generate one image for each scene.
        """

        logger.info(
            "Generating images for %d scene(s).",
            len(video.scenes),
        )

        for scene in video.scenes:

            logger.info(
                "Generating image for Scene %d.",
                scene.id,
            )

            parameters = {
                "prompt": scene.image_prompt,
                "negative_prompt": "",
                "seed": random.getrandbits(64),
                "steps": 30,
                "cfg": 7,
                "width": 1024,
                "height": 1024,
            }

            images = self._image_service.generate_image(
                workflow_name="txt2img",
                parameters=parameters,
            )

            if not images:
                raise RuntimeError(
                    f"No image returned for Scene {scene.id}."
                )

            scene.image_path = images[0]

            logger.info(
                "Scene %d image saved to %s",
                scene.id,
                scene.image_path,
            )