"""
comfyui.py

ComfyUI-related exceptions.
"""

from __future__ import annotations

from backend.exceptions.base import AtlasAIError


class ComfyUIError(AtlasAIError):
    """
    Base exception for ComfyUI-related errors.
    """


class ComfyUIConnectionError(ComfyUIError):
    """
    Raised when the ComfyUI server cannot be reached.
    """


class GenerationTimeoutError(ComfyUIError):
    """
    Raised when a generation exceeds the allowed timeout.
    """


class ImageDownloadError(ComfyUIError):
    """
    Raised when generated images cannot be downloaded.
    """