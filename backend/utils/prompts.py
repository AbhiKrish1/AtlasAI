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
        }}
    ]
}}
"""