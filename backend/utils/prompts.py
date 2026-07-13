"""
Prompt templates used throughout AtlasAI.
"""

CONTENT_PROMPT = """
You are an expert YouTube Shorts creator.

Create a complete YouTube Shorts content plan.

Topic:
{topic}

Requirements:

- Maximum 35 seconds.
- Strong hook.
- Conversational tone.
- Easy English.
- Exactly 5 scenes.
- Each scene should last 6–8 seconds.
- End with a call to action.
- The final scene MUST include the call to action naturally.

Return ONLY valid JSON.

{{
    "title": "",
    "hook": "",
    "script": "",
    "estimated_duration": 35,
    "scenes": [
        {{
            "scene_number": 1,
            "duration": 7,
            "narration": ""
        }},
        {{
            "scene_number": 2,
            "duration": 7,
            "narration": ""
        }},
        {{
            "scene_number": 3,
            "duration": 7,
            "narration": ""
        }},
        {{
            "scene_number": 4,
            "duration": 7,
            "narration": ""
        }},
        {{
            "scene_number": 5,
            "duration": 7,
            "narration": ""
        }}
    ]
}}
"""


PROMPT_GENERATOR_PROMPT = """
You are an award-winning cinematic concept artist.

Your task is to convert each narration scene into a detailed visual description
that can be used by an AI image generation model.

Requirements:

- Focus ONLY on what should appear visually.
- Do NOT describe camera movement.
- Do NOT include image quality terms like "8K", "masterpiece", or "cinematic".
- Do NOT include negative prompts.
- One prompt per scene.
- Preserve the order of the scenes.

Return ONLY valid JSON.

Example:

{{
    "prompts": [
        {{
            "scene_number": 1,
            "positive_prompt": "A massive black hole bending spacetime with glowing stars surrounding it",
            "negative_prompt": ""
        }}
    ]
}}

Scenes:

{scenes}
"""