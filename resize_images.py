from src.proportional_image_resizer import ProportionalImageResizer
from src.face_detector import FaceDetector
from src.image_processor import ImageProcessor
from config import Config
import cv2
import os
import time

def main():
    input_directory = Config.APPROVED_IMAGES_DIR
    output_directory = Config.CROPPED_IMAGES_DIR

    os.makedirs(output_directory, exist_ok=True)

    print("🔧 Usando bgremover directamente")
    print("=" * 50)
    
    # Contar imágenes de entrada
    total_images = 0
    for root, _, files in os.walk(input_directory):
        for filename in files:
            if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                total_images += 1
    
    print(f"📊 Total de imágenes a procesar: {total_images}")
    print("⏱️ Iniciando procesamiento...")
    
    # Iniciar timer
    start_time = time.time()
    
    image_resizer = ProportionalImageResizer()
    face_detector = FaceDetector(cv2.data.haarcascades + Config.HAAR_CASCADE_PATH)

    # proceso las imágenes directamente con bgremover integrado
    processor = ImageProcessor(image_resizer, face_detector)
    processor.process_images_with_bgremover(input_directory, output_directory)
    
    # Calcular tiempo total
    end_time = time.time()
    total_time = end_time - start_time
    
    # Mostrar estadísticas
    print("\n" + "=" * 50)
    print("📈 ESTADÍSTICAS DE PROCESAMIENTO")
    print("=" * 50)
    print(f"⏱️ Tiempo total: {total_time:.2f} segundos")
    print(f"📸 Imágenes procesadas: {total_images}")
    if total_images > 0:
        avg_time = total_time / total_images
        print(f"⚡ Tiempo promedio por imagen: {avg_time:.2f} segundos")
        print(f"🚀 Velocidad: {total_images/total_time:.2f} imágenes/segundo")
    print("=" * 50)

if __name__ == "__main__":
    main()