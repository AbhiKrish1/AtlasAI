"""
AtlasProject

Represents the complete state of a video generation project.
"""

from pydantic import BaseModel,Field

from backend.models.content import ContentPlan
from backend.models.prompt import PromptPlan
from backend.models.image import ImageSet
from backend.models.voice import VoiceTrack
from backend.models.video import VideoProject


class ProjectStatus(BaseModel):
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
    Represents one AtlasAI generation project.
    """

    topic: str

    progress: ProjectStatus = Field(default_factory=ProjectStatus)

    content: ContentPlan | None = None

    prompts: PromptPlan | None = None

    images: ImageSet | None = None

    voice: VoiceTrack | None = None

    video: VideoProject | None = None