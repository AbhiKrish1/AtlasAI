"""
Atlas Pipeline

Coordinates the entire generation workflow.
"""

from backend.generators.content_generator import ContentGenerator
from backend.models.atlas_project import AtlasProject


class AtlasPipeline:
    """
    Main orchestration pipeline.
    """

    def __init__(self):
        self.content_generator = ContentGenerator()

    def generate(
        self,
        topic: str,
    ) -> AtlasProject:

        project = AtlasProject(topic=topic)

        project.content = self.content_generator.generate(
            project.topic
        )

        project.progress.content_generated = True

        return project