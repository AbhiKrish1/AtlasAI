"""
AtlasAI

Module:
    comfyui_client.py

Responsibility:
    Communicate with the ComfyUI HTTP API.

Dependencies:
    Requests
    ComfyUI Exceptions
    Logger

Last Updated:
    Sprint 3
"""

from __future__ import annotations

import time
from typing import Any

import requests
from requests import RequestException

from backend.exceptions import (
    ComfyUIConnectionError,
    GenerationTimeoutError,
)
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class ComfyUIClient:
    """
    Client for the ComfyUI HTTP API.
    """

    def __init__(
        self,
        base_url: str = "http://127.0.0.1:8188",
        timeout: int = 30,
    ):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def queue_prompt(
        self,
        workflow: dict[str, Any],
    ) -> str:
        """
        Queue a workflow for execution.
        """

        logger.info("Queueing workflow for generation.")

        try:
            response = requests.post(
                f"{self.base_url}/prompt",
                json={"prompt": workflow},
                timeout=self.timeout,
            )

            response.raise_for_status()

        except RequestException as exc:
            logger.error("Failed to queue workflow.")

            raise ComfyUIConnectionError(
                "Failed to queue workflow."
            ) from exc

        prompt_id = response.json().get("prompt_id")

        if not prompt_id:
            logger.error(
                "ComfyUI returned an invalid prompt ID."
            )

            raise ComfyUIConnectionError(
                "ComfyUI returned an invalid response."
            )

        logger.info(
            "Queued workflow with prompt ID '%s'.",
            prompt_id,
        )

        return prompt_id

    def wait_for_completion(
        self,
        prompt_id: str,
        poll_interval: float = 1.0,
        timeout: int = 300,
    ) -> dict[str, Any]:
        """
        Wait until generation completes.
        """

        logger.info(
            "Waiting for prompt '%s' to complete.",
            prompt_id,
        )

        start = time.time()

        while True:
            history = self._get_history_entry(prompt_id)

            if history is not None:
                logger.info(
                    "Generation completed for prompt '%s'.",
                    prompt_id,
                )

                return history

            if time.time() - start >= timeout:
                logger.error(
                    "Generation timed out for prompt '%s'.",
                    prompt_id,
                )

                raise GenerationTimeoutError(
                    f"Generation exceeded {timeout} seconds."
                )

            time.sleep(poll_interval)

    def interrupt(self) -> None:
        """
        Interrupt the current generation.
        """

        logger.info("Interrupting generation.")

        try:
            response = requests.post(
                f"{self.base_url}/interrupt",
                timeout=self.timeout,
            )

            response.raise_for_status()

            logger.info("Generation interrupted.")

        except RequestException as exc:
            logger.error(
                "Failed to interrupt generation."
            )

            raise ComfyUIConnectionError(
                "Failed to interrupt generation."
            ) from exc

    def is_available(self) -> bool:
        """
        Check whether ComfyUI is reachable.
        """

        try:
            response = requests.get(
                f"{self.base_url}/system_stats",
                timeout=3,
            )

            return response.status_code == 200

        except RequestException:
            return False

    def get_history(
        self,
        prompt_id: str,
    ) -> dict[str, Any]:
        """
        Retrieve workflow history.
        """

        try:
            response = requests.get(
                f"{self.base_url}/history/{prompt_id}",
                timeout=self.timeout,
            )

            response.raise_for_status()

            return response.json()

        except RequestException as exc:
            logger.error(
                "Failed to retrieve history for prompt '%s'.",
                prompt_id,
            )

            raise ComfyUIConnectionError(
                "Failed to retrieve workflow history."
            ) from exc

    def _get_history_entry(
        self,
        prompt_id: str,
    ) -> dict[str, Any] | None:
        """
        Return a history entry if generation has completed.
        """

        history = self.get_history(prompt_id)

        return history.get(prompt_id)