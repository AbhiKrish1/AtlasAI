"""
AtlasAI

Module:
    test_generate_image.py

Responsibility:
    Integration tests for the image generation endpoint.

Last Updated:
    Sprint 4
"""

from __future__ import annotations

from fastapi.testclient import TestClient

from backend.api.app import app


client = TestClient(app)


REQUEST = {
    "workflow_name": "txt2img",
    "parameters": {
        "prompt": (
            "A cinematic photograph of a golden retriever "
            "wearing sunglasses on a beach, ultra realistic"
        ),
        "negative_prompt": "",
        "seed": 42,
        "steps": 10,
        "cfg": 7,
        "width": 512,
        "height": 512,
    },
}


def test_generate_image_endpoint() -> None:
    """
    Verify that the image generation endpoint completes
    successfully and returns generated image paths.
    """

    response = client.post(
        "/generate-image",
        json=REQUEST,
    )

    assert response.status_code == 200

    data = response.json()

    assert data["success"] is True
    assert "images" in data
    assert isinstance(data["images"], list)
    assert len(data["images"]) > 0

    for image in data["images"]:
        assert isinstance(image, str)
        assert image != ""

    assert data["message"] == (
        "Image generation completed successfully."
    )