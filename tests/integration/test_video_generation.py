from backend.ai.llm.ollama_client import OllamaClient
from backend.services.script_generation_service import (
    ScriptGenerationService,
)
from backend.services.video_generation_service import (
    VideoGenerationService,
)


def main():

    llm = OllamaClient()

    script_service = ScriptGenerationService(llm)

    video_service = VideoGenerationService(script_service)

    video = video_service.generate_video(
        "Top 5 Facts About Black Holes"
    )

    print()

    print("=" * 80)
    print(video.title)
    print("=" * 80)

    print()

    print("Narration Audio")
    print("-" * 80)
    print(video.audio_path)

    if video.audio_path is not None:
        print(f"Exists: {video.audio_path.exists()}")

    for scene in video.scenes:

        print()

        print(f"Scene {scene.id}")

        print(scene.narration)

        print()

        print(scene.image_prompt)

        print()

        print(scene.image_path)

    # ------------------------------------------------------------------
    # Basic integration assertions
    # ------------------------------------------------------------------

    assert video.audio_path is not None

    assert video.audio_path.exists()

    assert len(video.scenes) > 0

    for scene in video.scenes:

        assert scene.image_path is not None

        assert scene.image_path.exists()

    print()

    print("=" * 80)
    print("Sprint 6A integration test passed.")
    print("=" * 80)


if __name__ == "__main__":
    main()