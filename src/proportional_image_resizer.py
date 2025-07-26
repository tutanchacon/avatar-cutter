from PIL import Image
from src.image_resizer import ImageResizer

class ProportionalImageResizer(ImageResizer):
    def resize(self, image: Image.Image, max_width: int, max_height: int) -> Image.Image:
        width, height = image.size
        aspect_ratio = width / height

        if width > max_width or height > max_height:
            if aspect_ratio > (max_width / max_height):
                new_width = max_width
                new_height = int(max_width / aspect_ratio)
            else:
                new_height = max_height
                new_width = int(max_height * aspect_ratio)

            image = image.resize((new_width, new_height), Image.LANCZOS)
        
        return image
