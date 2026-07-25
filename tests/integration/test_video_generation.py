"""
AtlasAI

Module:
    test_video_generation.py

Responsibility:
    End-to-end integration test for the complete
    AtlasAI video generation pipeline.

Last Updated:
    Sprint 7A
"""

from __future__ import annotations

from pathlib import Path

import pytest

from backend.ai.llm.ollama_client import OllamaClient
from backend.services.script_generation_service import (
    ScriptGenerationService,
)
from backend.services.image_engine_service import (
    ImageEngineService,
)
from backend.services.narration_service import (
    NarrationService,
)
from backend.services.subtitle_service import (
    SubtitleService,
)
from backend.services.video_assembler_service import (
    VideoAssemblerService,
)


@pytest.mark.integration
def test_video_generation() -> None:
    """
    Full end-to-end pipeline with diagnostics.
    """

    topic = "Penis"

    llm = OllamaClient()

    script_service = ScriptGenerationService(llm)
    image_service = ImageEngineService()
    subtitle_service = SubtitleService()
    narration_service = NarrationService()
    assembler = VideoAssemblerService()

    print("\nGenerating script...")
    script = script_service.generate_script(topic)

    print("\nScene Durations")
    print("-" * 40)

    total_duration = 0.0

    for scene in script.scenes:
        print(
            f"Scene {scene.id}: "
            f"{scene.duration:.2f}s | "
            f"{len(scene.narration.split())} words"
        )
        total_duration += scene.duration

    print("-" * 40)
    print(f"Estimated total duration: {total_duration:.2f}s")

    print("\nGenerating subtitles...")
    subtitle_path = subtitle_service.generate_subtitles(script)

    print(f"Subtitle file : {subtitle_path}")

    assert subtitle_path.exists()
    assert subtitle_path.stat().st_size > 0

    print("\nGenerating images...")
    script = image_service.generate_images_for_script(script)

    print("\nGenerating narration...")
    video = narration_service.create_video(script)

    print(f"Audio file : {video.audio_path}")

    output_path = assembler.assemble(video)

    print()
    print("===================================")
    print(" Full Pipeline Integration Test")
    print("===================================")
    print(f"Topic              : {topic}")
    print(f"Estimated Duration : {total_duration:.2f}s")
    print(f"Subtitle           : {subtitle_path}")
    print(f"Output             : {output_path}")
    print(f"Size               : {output_path.stat().st_size} bytes")
    print("Status             : PASS")
    print("===================================")

    assert isinstance(output_path, Path)
    assert output_path.exists()
    assert output_path.stat().st_size > 0