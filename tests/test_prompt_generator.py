from backend.generators.content_generator import ContentGenerator
from backend.generators.prompt_generator import PromptGenerator

topic = "Top 5 Facts About Black Holes"

content = ContentGenerator().generate(topic)

generator = PromptGenerator()

prompts = generator.generate(content)

print()

for prompt in prompts.prompts:
    print("=" * 60)
    print(prompt.scene_number)
    print()
    print(prompt.positive_prompt)
    print()
    print(prompt.negative_prompt)