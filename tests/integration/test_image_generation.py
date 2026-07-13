"""
AtlasAI

Module:
    test_image_generation.py

Responsibility:
    End-to-end integration test for the image generation pipeline.

Last Updated:
    Sprint 3
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

# Allow running the script directly:
# python tests/integration/test_image_generation.py
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.comfyui_client import ComfyUIClient
from backend.services.image_engine_service import ImageEngineService
from backend.services.workflow_loader import WorkflowLoader


WORKFLOW_NAME = "txt2img"

PARAMETERS = {
    "prompt": "A cinematic photograph of a golden retriever wearing sunglasses on a beach, ultra realistic",
    "negative_prompt": "",
    "seed": 42,
    "steps": 10,
    "cfg": 7,
    "width": 512,
    "height": 512,
}


def print_result(
    passed: bool,
    message: str,
) -> None:
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {message}")


def main() -> None:
    print("=" * 60)
    print("AtlasAI Sprint 3 Integration Test")
    print("=" * 60)

    start_time = time.perf_counter()

    loader = WorkflowLoader()
    client = ComfyUIClient()
    engine = ImageEngineService(
        workflow_loader=loader,
        comfy_client=client,
    )

    try:
        # --------------------------------------------------
        # Check ComfyUI
        # --------------------------------------------------

        if not client.is_available():
            raise RuntimeError(
                "ComfyUI server is not running."
            )

        print_result(
            True,
            "ComfyUI server reachable",
        )

        # --------------------------------------------------
        # Check workflow
        # --------------------------------------------------

        if not loader.exists(WORKFLOW_NAME):
            raise RuntimeError(
                f"Workflow '{WORKFLOW_NAME}' not found."
            )

        print_result(
            True,
            "Workflow package found",
        )

        # --------------------------------------------------
        # Generate image
        # --------------------------------------------------

        images = engine.generate_image(
            workflow_name=WORKFLOW_NAME,
            parameters=PARAMETERS,
        )

        print_result(
            True,
            "Image generation completed",
        )

        # --------------------------------------------------
        # Verify downloads
        # --------------------------------------------------

        if not images:
            raise RuntimeError(
                "No images were downloaded."
            )

        print_result(
            True,
            f"Downloaded {len(images)} image(s)",
        )

        # --------------------------------------------------
        # Verify files
        # --------------------------------------------------

        for image in images:
            if not image.exists():
                raise RuntimeError(
                    f"Missing output file: {image}"
                )

        print_result(
            True,
            "Verified output file(s)",
        )

        elapsed = time.perf_counter() - start_time

        print()
        print(f"Execution Time : {elapsed:.2f} s")
        print()
        print("=" * 60)
        print("OVERALL RESULT : PASS")
        print("=" * 60)

    except Exception as exc:
        elapsed = time.perf_counter() - start_time

        print_result(
            False,
            "Integration test failed",
        )

        print()
        print("Reason:")
        print(f"{type(exc).__name__}: {exc}")

        print()
        print(f"Execution Time : {elapsed:.2f} s")
        print()

        print("=" * 60)
        print("OVERALL RESULT : FAIL")
        print("=" * 60)

        raise


if __name__ == "__main__":
    main()