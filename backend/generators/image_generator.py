class ImageGenerator:

    def generate(project):

        for prompt in project.prompts.prompts:

            image = image_engine.generate_image(
                prompt.positive_prompt,
                output_path
            )

            project.images.images.append(image)

        project.progress.images_generated = True