"""
workflow_template.py

Represents a workflow package loaded from disk.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class WorkflowTemplate:
    """
    A workflow package consisting of the workflow definition and
    its runtime parameter mapping.
    """

    workflow: dict[str, Any]
    mapping: dict[str, Any]