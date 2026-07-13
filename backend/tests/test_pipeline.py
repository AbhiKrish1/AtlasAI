from backend.pipeline.atlas_pipeline import AtlasPipeline

pipeline = AtlasPipeline()

project = pipeline.generate(
    "Top 5 Facts About Black Holes"
)

print()

print("Project ID:")
print(project.project_id)

print()

print("Output Directory:")
print(project.output_dir)

print()

print(project.content.title)

print()

print(project.progress)