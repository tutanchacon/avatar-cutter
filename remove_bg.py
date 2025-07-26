from src.remove_bg_service import RemoveBgService
from src.proportional_image_resizer import ProportionalImageResizer
from src.face_detector import FaceDetector
from src.image_processor import ImageProcessor
from config import Config
import cv2
import os

def main():
    input_directory = Config.APPROVED_IMAGES_DIR
    output_directory = Config.BG_REMOVED_DIR

    os.makedirs(output_directory, exist_ok=True)

    # Usar configuración segura para API key
    api_key = Config.get_remove_bg_api_key()
    background_remover = RemoveBgService(api_key=api_key)
    image_resizer = ProportionalImageResizer()
    face_detector = FaceDetector(cv2.data.haarcascades + Config.HAAR_CASCADE_PATH)

    # proceso las imágenes para remover el fondo
    processor = ImageProcessor(background_remover, image_resizer, face_detector)
    processor.remove_background_batch(input_directory, output_directory)

if __name__ == "__main__":
    main()