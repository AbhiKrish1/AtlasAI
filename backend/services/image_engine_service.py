class ImageEngineService:

    def generate_image(
        self,
        prompt: str,
        output_path: Path
    ) -> Path:
        ...