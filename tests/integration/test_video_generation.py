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

    for scene in video.scenes:

        print()

        print(f"Scene {scene.id}")

        print(scene.narration)

        print()

        print(scene.image_prompt)

        print()

        print(scene.image_path)


if __name__ == "__main__":
    main()