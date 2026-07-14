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
    Sprint 4
"""

from __future__ import annotations

import time
from typing import Any

import requests
from requests import RequestException, Response

from backend.config import settings
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
        base_url: str | None = None,
        timeout: int | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = (
            base_url
            if base_url is not None
            else settings.COMFYUI_URL
        ).rstrip("/")

        self.timeout = (
            timeout
            if timeout is not None
            else settings.COMFYUI_TIMEOUT
        )

        self.session = (
            session
            if session is not None
            else requests.Session()
        )

    def queue_prompt(
        self,
        workflow: dict[str, Any],
    ) -> str:
        """
        Queue a workflow for execution.
        """

        logger.info("Queueing workflow for generation.")

        try:
            response = self._request(
                "POST",
                "/prompt",
                json={"prompt": workflow},
            )

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
            self._request(
                "POST",
                "/interrupt",
            )

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
            response = self.session.get(
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
            response = self._request(
                "GET",
                f"/history/{prompt_id}",
            )

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

    def _request(
        self,
        method: str,
        endpoint: str,
        **kwargs: Any,
    ) -> Response:
        """
        Execute an HTTP request using the configured session.
        """

        response = self.session.request(
            method=method,
            url=f"{self.base_url}{endpoint}",
            timeout=self.timeout,
            **kwargs,
        )

        response.raise_for_status()

        return response