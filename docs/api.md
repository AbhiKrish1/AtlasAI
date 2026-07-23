# AtlasAI Backend API

## Overview

The AtlasAI Backend provides REST API endpoints for image generation using ComfyUI workflows.

Base URL:

```
http://127.0.0.1:8000
```

Swagger Documentation:

```
http://127.0.0.1:8000/docs
```

---

# Health Endpoint

## GET /health

Checks whether the backend is running.

### Request

```
GET /health
```

### Response

```json
{
    "status": "ok",
    "service": "AtlasAI Backend"
}
```

---

# Generate Image Endpoint

## POST /generate-image

Generates one or more images using a workflow package.

### Request

```json
{
    "workflow_name": "txt2img",
    "parameters": {
        "prompt": "A futuristic city at sunset",
        "negative_prompt": "",
        "seed": 42,
        "steps": 10,
        "cfg": 7,
        "width": 512,
        "height": 512
    }
}
```

---

### Successful Response

```json
{
    "success": true,
    "images": [
        "generated_images/ComfyUI_00121_.png"
    ],
    "message": "Image generation completed successfully."
}
```

---

### Error Response

```json
{
    "detail": "Workflow 'txt2img' not found."
}
```

or

```json
{
    "detail": "ComfyUI server is unavailable."
}
```

depending on the failure.

---

# Testing

Integration Test

```bash
python tests/integration/test_image_generation.py
```

Health API Test

```bash
python -m pytest tests/api/test_health.py
```

Generate Image API Test

```bash
python -m pytest tests/api/test_generate_image.py
```

Run all API tests

```bash
python -m pytest tests/api
```

---

# Current Workflow

AtlasAI currently uses the following workflow package:

```
resources/workflows/txt2img/
```

The workflow is dynamically loaded by the backend and runtime parameters are injected through `mapping.json`.

---

# Architecture

```
FastAPI
    ↓
GenerationService
    ↓
ImageEngineService
    ↓
WorkflowLoader
    ↓
ComfyUIClient
    ↓
ComfyUI
    ↓
ImageDownloader
```

---

# Status

Sprint 4 Backend API Complete

Features:

- FastAPI backend
- Swagger documentation
- Workflow loading
- Runtime parameter injection
- ComfyUI integration
- Image downloading
- Health endpoint
- Image generation endpoint
- Automated integration tests
- Automated API tests