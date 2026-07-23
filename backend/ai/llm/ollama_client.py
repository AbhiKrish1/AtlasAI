"""
AtlasAI

Module:
    ollama_client.py

Responsibility:
    Provides a client for interacting with a local Ollama server.

Last Updated:
    Sprint 5
"""

from __future__ import annotations

import logging

import ollama

from backend.ai.llm.base import BaseLLMClient

logger = logging.getLogger(__name__)


class OllamaClient(BaseLLMClient):
    """
    Client for communicating with a local Ollama instance.
    """

    def __init__(self, model: str = "qwen3:8b"):
        self._model = model

    def generate(self, prompt: str) -> str:
        """
        Generate a response from the configured Ollama model.

        Args:
            prompt: Input prompt.

        Returns:
            Generated response text.

        Raises:
            RuntimeError:
                If Ollama fails to generate a response.
        """

        logger.info("Sending prompt to Ollama using model '%s'.", self._model)

        try:
            response = ollama.chat(
                model=self._model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
            )

            content = response["message"]["content"].strip()

            logger.info(
                "Received response from Ollama (%d characters).",
                len(content),
            )

            return content

        except Exception as exc:
            logger.exception("Failed to generate response from Ollama.")
            raise RuntimeError(
                "Unable to communicate with the Ollama server."
            ) from exc