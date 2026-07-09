from backend.pipeline.atlas_pipeline import AtlasPipeline


pipeline = AtlasPipeline()

project = pipeline.generate(
    "Top 5 Facts About Black Holes"
)

print()

print(project.content)

print()

print(project.progress)