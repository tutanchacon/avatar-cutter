"""
Avatar Image Processor - Paquete de procesamiento de imágenes de avatar

Este paquete proporciona herramientas para:
- Remoción de fondo de imágenes
- Detección facial
- Redimensionado proporcional de imágenes
- Procesamiento por lotes
"""

__version__ = "1.0.0"
__author__ = "Avatar Image Processor Team"

from .image_processor import ImageProcessor
from .face_detector import FaceDetector
from .remove_bg_service import RemoveBgService
from .proportional_image_resizer import ProportionalImageResizer
from .avatar_size import AvatarSize

__all__ = [
    'ImageProcessor',
    'FaceDetector', 
    'RemoveBgService',
    'ProportionalImageResizer',
    'AvatarSize'
]
