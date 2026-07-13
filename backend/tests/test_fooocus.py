"""
Tests AtlasAI's connection to Fooocus.

This file is temporary and only validates the integration.
"""

from gradio_client import Client

print("Connecting to Fooocus...")

client = Client("http://127.0.0.1:7865")

print("Connected!")

print("Sending generation request...")

result = client.predict(
    # ---------- Basic Generation ----------
    True,
    "A cinematic black hole in deep space, photorealistic, volumetric lighting",
    "low quality, blurry, watermark",
    ["Fooocus V2"],
    "Quality",
    '704×1408 <span style="color: grey;"> ∣ 1:2</span>',
    1,
    "png",
    "",
    False,

    # ---------- Basic Settings ----------
    2,
    4,

    "realisticStockPhoto_v20.safetensors",
    "None",
    0.8,

    # ---------- LoRAs ----------
    False, "None", 1.0,
    False, "None", 1.0,
    False, "None", 1.0,
    False, "None", 1.0,
    False, "None", 1.0,

    # Everything else remains exactly as the generated defaults
    # (we'll add them only if Fooocus asks for them)

    fn_index=67,
)

print()
print("========== RESULT ==========")
print(result)