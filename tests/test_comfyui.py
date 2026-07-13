import json
import time
import uuid
from pathlib import Path

import requests


COMFYUI_URL = "http://127.0.0.1:8188"

WORKFLOW_PATH = Path(
    "backend/resources/workflows/txt2img.json"
)

OUTPUT_DIR = Path("outputs/comfyui_test")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def load_workflow():

    with open(WORKFLOW_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def queue_prompt(workflow):

    client_id = str(uuid.uuid4())

    response = requests.post(
        f"{COMFYUI_URL}/prompt",
        json={
            "prompt": workflow,
            "client_id": client_id,
        },
    )

    response.raise_for_status()

    return response.json()["prompt_id"]


def wait_for_completion(prompt_id):

    print("Waiting for image generation...")

    while True:

        history = requests.get(
            f"{COMFYUI_URL}/history/{prompt_id}"
        ).json()

        if prompt_id in history:
            return history[prompt_id]

        time.sleep(1)


def download_image(filename, subfolder):

    response = requests.get(
        f"{COMFYUI_URL}/view",
        params={
            "filename": filename,
            "subfolder": subfolder,
            "type": "output",
        },
    )

    response.raise_for_status()

    destination = OUTPUT_DIR / filename

    with open(destination, "wb") as f:
        f.write(response.content)

    return destination


def main():

    workflow = load_workflow()

    workflow["6"]["inputs"]["text"] = (
        "A cinematic black hole in deep space, "
        "ultra detailed, realistic, volumetric lighting, "
        "glowing accretion disk, masterpiece, 8k"
    )

    workflow["7"]["inputs"]["text"] = (
        "low quality, blurry, watermark, text"
    )

    prompt_id = queue_prompt(workflow)

    history = wait_for_completion(prompt_id)

    outputs = history["outputs"]

    for node in outputs.values():

        if "images" not in node:
            continue

        for image in node["images"]:

            path = download_image(
                image["filename"],
                image["subfolder"],
            )

            print()
            print("=" * 60)
            print("SUCCESS")
            print(path)
            print("=" * 60)
            return


if __name__ == "__main__":
    main()