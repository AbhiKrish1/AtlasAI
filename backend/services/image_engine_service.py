"""
AtlasAI

Module:
    image_engine_service.py

Responsibility:
    Coordinate the complete image generation workflow.

Dependencies:
    WorkflowLoader
    ComfyUIClient
    ImageDownloader
    WorkflowTemplate
    Logger

Last Updated:
    Sprint 3
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from backend.exceptions import (
    InvalidWorkflowParameterError,
    WorkflowMappingError,
)
from backend.models.workflow_template import WorkflowTemplate
from backend.services.comfyui_client import ComfyUIClient
from backend.services.image_downloader import ImageDownloader
from backend.services.workflow_loader import WorkflowLoader
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ImageEngineService:
    """
    Coordinates image generation.
    """

    def __init__(
        self,
        workflow_loader: WorkflowLoader | None = None,
        comfy_client: ComfyUIClient | None = None,
        downloader: ImageDownloader | None = None,
    ):
        self.workflow_loader = workflow_loader or WorkflowLoader()
        self.comfy_client = comfy_client or ComfyUIClient()
        self.downloader = downloader or ImageDownloader()

    def generate_image(
        self,
        workflow_name: str,
        parameters: dict[str, Any],
    ) -> list[Path]:
        """
        Generate images using a workflow package.
        """

        logger.info(
            "Starting image generation using workflow '%s'.",
            workflow_name,
        )

        logger.info("Preparing workflow.")
        template = self.workflow_loader.load(workflow_name)

        logger.info(
            "Injecting %d runtime parameter(s).",
            len(parameters),
        )
        self._populate_workflow(template, parameters)

        logger.info("Submitting workflow to ComfyUI.")
        prompt_id = self.comfy_client.queue_prompt(
            template.workflow
        )

        logger.info("Waiting for image generation.")
        history = self.comfy_client.wait_for_completion(
            prompt_id
        )

        logger.info("Downloading generated images.")
        images = self.downloader.download_images(
            history
        )

        logger.info(
            "Image generation completed successfully."
        )

        return images

    def _populate_workflow(
        self,
        template: WorkflowTemplate,
        parameters: dict[str, Any],
    ) -> None:
        """
        Populate workflow inputs.
        """

        for key, value in parameters.items():
            self._inject(
                template.workflow,
                template.mapping,
                key,
                value,
            )

    def _inject(
        self,
        workflow: dict[str, Any],
        mapping: dict[str, Any],
        key: str,
        value: Any,
    ) -> None:
        """
        Inject a runtime parameter.
        """

        if value is None:
            return

        if key not in mapping:
            logger.error(
                "Unknown workflow parameter '%s'.",
                key,
            )

            raise InvalidWorkflowParameterError(
                f"Unknown parameter '{key}'."
            )

        target = mapping[key]

        node = workflow.get(target["node"])

        if node is None:
            logger.error(
                "Workflow node '%s' does not exist.",
                target["node"],
            )

            raise WorkflowMappingError(
                f"Node '{target['node']}' does not exist."
            )

        inputs = node.get("inputs")

        if inputs is None:
            logger.error(
                "Workflow node '%s' has no inputs.",
                target["node"],
            )

            raise WorkflowMappingError(
                f"Node '{target['node']}' has no inputs."
            )

        field = target["field"]

        if field not in inputs:
            logger.error(
                "Workflow field '%s' does not exist.",
                field,
            )

            raise WorkflowMappingError(
                f"Field '{field}' does not exist."
            )

        inputs[field] = value