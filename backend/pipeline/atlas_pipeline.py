"""
Atlas Pipeline

Coordinates the complete AtlasAI workflow.
"""

from backend.config.settings import OUTPUT_DIR
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

        project = AtlasProject(
            topic=topic,
        )

        project.output_dir = (
            OUTPUT_DIR / project.project_id
        )

        project.output_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        project.content = self.content_generator.generate(
            project.topic
        )

        project.progress.content_generated = True

        return project