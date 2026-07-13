"""
AtlasAI exception hierarchy.

Import project exceptions from this package instead of individual modules.

Example:
    from backend.exceptions import WorkflowNotFoundError
"""

from backend.exceptions.base import AtlasAIError
from backend.exceptions.workflow import (
    InvalidWorkflowParameterError,
    WorkflowError,
    WorkflowMappingError,
    WorkflowNotFoundError,
)
from backend.exceptions.comfyui import (
    ComfyUIConnectionError,
    ComfyUIError,
    GenerationTimeoutError,
    ImageDownloadError,
)

__all__ = [
    "AtlasAIError",
    "WorkflowError",
    "WorkflowNotFoundError",
    "WorkflowMappingError",
    "InvalidWorkflowParameterError",
    "ComfyUIError",
    "ComfyUIConnectionError",
    "GenerationTimeoutError",
    "ImageDownloadError",
]