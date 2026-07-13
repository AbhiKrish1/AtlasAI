"""
AtlasAI

Module:
    workflow_loader.py

Responsibility:
    Load workflow packages from disk.

Dependencies:
    WorkflowTemplate
    Workflow Exceptions
    Logger

Last Updated:
    Sprint 3
"""

from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from backend.exceptions import (
    WorkflowMappingError,
    WorkflowNotFoundError,
)
from backend.models.workflow_template import WorkflowTemplate
from backend.utils.logger import get_logger

logger = get_logger(__name__)


class WorkflowLoader:
    """
    Loads workflow packages from disk.
    """

    def __init__(
        self,
        workflow_dir: str | Path | None = None,
    ):
        if workflow_dir is None:
            root = Path(__file__).resolve().parents[2]
            workflow_dir = root / "resources" / "workflows"

        self.workflow_dir = Path(workflow_dir)

    def load(
        self,
        workflow_name: str,
    ) -> WorkflowTemplate:
        """
        Load a workflow package.
        """

        logger.info(
            "Loading workflow '%s'.",
            workflow_name,
        )

        workflow_folder = self.workflow_dir / workflow_name

        if not workflow_folder.exists():
            logger.error(
                "Workflow '%s' does not exist.",
                workflow_name,
            )

            raise WorkflowNotFoundError(
                f"Workflow '{workflow_name}' was not found."
            )

        workflow = self._load_json(
            workflow_folder / "workflow.json"
        )

        mapping = self._load_json(
            workflow_folder / "mapping.json"
        )

        logger.info(
            "Loaded workflow '%s'.",
            workflow_name,
        )

        return WorkflowTemplate(
            workflow=copy.deepcopy(workflow),
            mapping=copy.deepcopy(mapping),
        )

    def exists(
        self,
        workflow_name: str,
    ) -> bool:
        """
        Check whether a workflow package exists.
        """

        exists = (
            self.workflow_dir
            / workflow_name
            / "workflow.json"
        ).exists()

        logger.debug(
            "Workflow '%s' exists: %s",
            workflow_name,
            exists,
        )

        return exists

    def list_workflows(
        self,
    ) -> list[str]:
        """
        Return available workflow package names.
        """

        if not self.workflow_dir.exists():
            logger.warning(
                "Workflow directory '%s' does not exist.",
                self.workflow_dir,
            )
            return []

        workflows = sorted(
            folder.name
            for folder in self.workflow_dir.iterdir()
            if folder.is_dir()
        )

        logger.info(
            "Discovered %d workflow package(s).",
            len(workflows),
        )

        return workflows

    def _load_json(
        self,
        path: Path,
    ) -> dict[str, Any]:
        """
        Load and validate a JSON resource.
        """

        if not path.exists():
            logger.error(
                "Required workflow file '%s' was not found.",
                path,
            )

            raise WorkflowNotFoundError(
                f"Required file not found: {path.name}"
            )

        try:
            with path.open(
                "r",
                encoding="utf-8",
            ) as file:
                return json.load(file)

        except json.JSONDecodeError as exc:
            logger.error(
                "Invalid JSON in '%s'.",
                path,
            )

            raise WorkflowMappingError(
                f"Invalid JSON in '{path.name}'."
            ) from exc