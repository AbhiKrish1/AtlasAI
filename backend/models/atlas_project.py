"""
AtlasProject

Represents the complete state of a video generation project.
"""

from pathlib import Path
from uuid import uuid4

from pydantic import BaseModel, Field

from backend.models.content import ContentPlan
from backend.models.prompt import PromptPlan
from backend.models.image import ImageSet
from backend.models.voice import VoiceTrack
from backend.models.video import VideoProject


class ProjectProgress(BaseModel):
    """
    Tracks the progress of the generation pipeline.
    """

    content_generated: bool = False

    prompts_generated: bool = False

    images_generated: bool = False

    voice_generated: bool = False

    video_generated: bool = False


class AtlasProject(BaseModel):
    """
    Represents a single AtlasAI generation project.
    """

    project_id: str = Field(
        default_factory=lambda: str(uuid4())
    )

    topic: str

    output_dir: Path | None = None

    progress: ProjectProgress = Field(
        default_factory=ProjectProgress
    )

    content: ContentPlan | None = None

    prompts: PromptPlan | None = None

    images: ImageSet | None = None

    voice: VoiceTrack | None = None

    video: VideoProject | None = None