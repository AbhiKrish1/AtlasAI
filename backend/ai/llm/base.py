"""
AtlasAI

Module:
    base.py

Responsibility:
    Defines the interface that all LLM clients must implement.

Last Updated:
    Sprint 5
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class BaseLLMClient(ABC):
    """
    Abstract base class for Large Language Model clients.
    """

    @abstractmethod
    def generate(self, prompt: str) -> str:
        """
        Generate a response for the given prompt.

        Args:
            prompt: The input prompt.

        Returns:
            The generated text response.
        """
        raise NotImplementedError