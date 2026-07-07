"""
Service responsible for communicating with the local Ollama server.
"""

from ollama import Client

from backend.config.settings import (
    OLLAMA_HOST,
    OLLAMA_MODEL,
)


class OllamaService:
    """
    Thin wrapper around Ollama.

    Other modules should never talk directly
    to the Ollama client.
    """

    def __init__(self):
        self.client = Client(host=OLLAMA_HOST)

    def generate(self, prompt: str) -> str:
        """
        Generate text using the configured model.
        """

        response = self.client.generate(
            model=OLLAMA_MODEL,
            prompt=prompt,
        )

        return response["response"]