"""
workflow.py

Workflow-related exceptions.
"""

from __future__ import annotations

from backend.exceptions.base import AtlasAIError


class WorkflowError(AtlasAIError):
    """
    Base exception for workflow-related errors.
    """


class WorkflowNotFoundError(WorkflowError):
    """
    Raised when a requested workflow package cannot be found.
    """


class WorkflowMappingError(WorkflowError):
    """
    Raised when a workflow mapping is missing or invalid.
    """


class InvalidWorkflowParameterError(WorkflowError):
    """
    Raised when an unknown or invalid workflow parameter is supplied.
    """