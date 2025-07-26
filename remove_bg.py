"""
⚠️ ARCHIVO DEPRECATED - YA NO SE USA
=====================================

Este script ya no es necesario. Ahora el procesamiento completo
(remoción de fondo + redimensionamiento) se hace en resize_images.py

Flujo actual:
p2_approvedimages → resize_images.py → p4_croppedimages
"""

from src.proportional_image_resizer import ProportionalImageResizer
from src.face_detector import FaceDetector
from src.image_processor import ImageProcessor
from config import Config
import cv2
import os

def main():
    print("⚠️ Este script ya no se usa.")
    print("💡 Usa resize_images.py que hace todo el procesamiento completo.")
    return
    
    # CÓDIGO DEPRECATED - NO SE EJECUTA
    input_directory = Config.APPROVED_IMAGES_DIR
    # output_directory = Config.BG_REMOVED_DIR  # Ya no existe

    os.makedirs(output_directory, exist_ok=True)

    print("🔧 Usando bgremover directamente para remover fondos")
    print("=" * 50)
    
    image_resizer = ProportionalImageResizer()
    face_detector = FaceDetector(cv2.data.haarcascades + Config.HAAR_CASCADE_PATH)

    # proceso las imágenes solo para remover el fondo
    processor = ImageProcessor(image_resizer, face_detector)
    processor.remove_background_batch(input_directory, output_directory)

if __name__ == "__main__":
    main()