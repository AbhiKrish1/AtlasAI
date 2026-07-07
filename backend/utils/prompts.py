"""
Prompt templates used throughout AtlasAI.
"""

SCRIPT_PROMPT = """
You are an expert YouTube Shorts script writer.

Your task is to create an engaging script.

Topic:
{topic}

Requirements:

- Maximum 35 seconds.
- Strong hook.
- Conversational tone.
- Easy English.
- Build curiosity.
- End with a call to action.

Return ONLY valid JSON.

{{
    "title": "",
    "hook": "",
    "script": "",
    "estimated_duration": 35
}}
"""