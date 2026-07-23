from backend.ai.llm.ollama_client import OllamaClient
from backend.services.script_generation_service import (
    ScriptGenerationService,
)


def main():
    topic = "Top 5 Facts About Black Holes"

    llm = OllamaClient()

    service = ScriptGenerationService(llm)

    script = service.generate_script(topic)

    print("\n========== SCRIPT ==========\n")

    print(f"Title: {script.title}\n")

    print("Scenes:\n")

    for scene in script.scenes:

        print(f"Scene {scene.id}")

        print(f"Duration: {scene.duration:.2f}s")

        print()

        print("Narration:")

        print(scene.narration)

        print()

        print("Image Prompt:")

        print(scene.image_prompt)

        print()

        print("-" * 80)


if __name__ == "__main__":
    main()