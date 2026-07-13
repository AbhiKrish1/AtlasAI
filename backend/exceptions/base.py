"""
base.py

Base exceptions for AtlasAI.

All custom exceptions should inherit from AtlasAIError either
directly or indirectly.
"""

from __future__ import annotations


class AtlasAIError(Exception):
    """
    Base exception for all AtlasAI-specific errors.
    """

    def __init__(self, message: str):
        super().__init__(message)