from src.proportional_image_resizer import ProportionalImageResizer
from src.face_detector import FaceDetector
from src.image_processor import ImageProcessor
from config import Config
import cv2
import os

def main():
    input_directory = Config.APPROVED_IMAGES_DIR
    output_directory = Config.CROPPED_IMAGES_DIR

    os.makedirs(output_directory, exist_ok=True)

    print("🔧 Usando bgremover directamente")
    print("=" * 50)
    
    image_resizer = ProportionalImageResizer()
    face_detector = FaceDetector(cv2.data.haarcascades + Config.HAAR_CASCADE_PATH)

    # proceso las imágenes directamente con bgremover integrado
    processor = ImageProcessor(image_resizer, face_detector)
    processor.process_images_with_bgremover(input_directory, output_directory)

if __name__ == "__main__":
    main()