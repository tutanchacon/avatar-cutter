from abc import ABC, abstractmethod
from PIL import Image

class ImageResizer(ABC):
    @abstractmethod
    def resize(self, image: Image.Image, max_width: int, max_height: int) -> Image.Image:
        pass