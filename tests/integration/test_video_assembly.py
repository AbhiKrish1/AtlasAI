"""
AtlasAI

Module:
    test_video_assembly.py

Responsibility:
    End-to-end integration test for the video assembly
    pipeline.

Last Updated:
    Sprint 6B
"""

from __future__ import annotations

from pathlib import Path

import pytest
from PIL import Image

from backend.models.scene import Scene
from backend.models.video import Video
from backend.services.video_assembler_service import (
    VideoAssemblerService,
)


def _create_test_image(
    path: Path,
    color: str,
) -> None:
    """
    Create a simple PNG image for testing.
    """

    image = Image.new(
        "RGB",
        (1080, 1920),
        color=color,
    )

    image.save(path)


@pytest.fixture
def sample_video(
    tmp_path: Path,
) -> Video:
    """
    Create a sample Video object containing two scenes.
    """

    image1 = tmp_path / "scene1.png"
    image2 = tmp_path / "scene2.png"

    _create_test_image(image1, "red")
    _create_test_image(image2, "blue")

    scenes = [
        Scene(
            id=1,
            narration="Scene one",
            image_prompt="Red image",
            duration=2.0,
            image_path=image1,
        ),
        Scene(
            id=2,
            narration="Scene two",
            image_prompt="Blue image",
            duration=2.0,
            image_path=image2,
        ),
    ]

    return Video(
        title="Integration Test Video",
        scenes=scenes,
    )


def test_video_assembly(
    tmp_path: Path,
    sample_video: Video,
) -> None:
    """
    Verify that the video assembly pipeline creates
    a playable MP4 from scene images.
    """

    assembler = VideoAssemblerService(
        output_directory=tmp_path,
    )

    output = assembler.assemble(
        sample_video,
    )

    assert output.exists()

    assert output.is_file()

    assert output.suffix == ".mp4"

    assert output.stat().st_size > 0

    expected = (
        tmp_path
        / "integration-test-video.mp4"
    )

    assert output == expected

    print()

    print("===================================")
    print(" Video Assembly Integration Test")
    print("===================================")
    print(f"Output : {output}")
    print(f"Size   : {output.stat().st_size} bytes")
    print("Status : PASS")
    print("===================================")