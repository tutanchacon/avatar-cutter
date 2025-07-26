from src.avatar_size import AvatarSize
from src.background_remover import BackgroundRemover
from src.image_resizer import ImageResizer
from src.face_detector import FaceDetector
import os
from PIL import Image

class ImageProcessor:
    def __init__(self, background_remover: BackgroundRemover, image_resizer: ImageResizer, face_detector: FaceDetector):
        self.background_remover = background_remover
        self.image_resizer = image_resizer
        self.face_detector = face_detector

    def remove_background_batch(self, input_dir: str, output_dir: str) -> None:
        for root, _, files in os.walk(input_dir):
            for filename in files:
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    relative_path = os.path.relpath(root, input_dir)
                    output_subdir = os.path.join(output_dir, relative_path)
                    os.makedirs(output_subdir, exist_ok=True)
                    self._remove_img_background(filename, root, output_subdir)

    def _remove_img_background(self, filename: str, input_dir: str, output_dir: str) -> None:
        input_image_path = os.path.join(input_dir, filename)
        output_image_path = os.path.join(output_dir, filename)
        
        # elimino el fondo
        self._remove_background(input_image_path, output_image_path)
        
    def resize_images(self, input_dir: str, output_dir: str) -> None:
        for root, _, files in os.walk(input_dir):
            for filename in files:
                if filename.lower().endswith('.png'):
                    relative_path = os.path.relpath(root, input_dir)
                    output_subdir = os.path.join(output_dir, relative_path)
                    os.makedirs(output_subdir, exist_ok=True)
                    
                    image_path = os.path.join(root, filename)
                    image = Image.open(image_path)
                    
                    # calculo el directorio destino
                    filename_wo_ext = os.path.splitext(filename)[0]
                    final_path = os.path.join(output_subdir, filename_wo_ext)

                    # redimensiono la imagen al tamaño máximo de 204x350
                    size = AvatarSize.S_204x350.value
                    resized_image_1 = self._resize_image(image, size[2], size[3])
                    
                    # redimesiono la imagen al tamaño máximo de 136x234
                    size = AvatarSize.S_136x234.value
                    resized_image_2 = self._resize_image(image, size[2], size[3])

                   
                    # genero los recortes para 86x86 y 38x38 partiendo de la posición de la cara
                    # pero si no es capaz de detectar la cara, no se generan los recortes y se loguea
                    # Uso el método optimizado para avatares de cuerpo completo
                    faceRect = self.face_detector.detect_face_center_rect_optimized(resized_image_1, (86, 86))
                    if faceRect is not None:
                        self._process_face(faceRect, resized_image_1, final_path)
                    else:
                        with open(os.path.join(output_dir, "log.txt"), "a") as log_file:
                                log_file.write(f"no se pudo procesar: {filename}\n")
                        # agrego el prefijo "error_" a output_dir y continúo el proceso+
                        final_path = os.path.join(output_subdir, f"error_{filename_wo_ext}")
                        
                                                    
                    # proceso las áreas del primer escalado
                    self._process_rect(AvatarSize.S_204x350, resized_image_1, final_path)
                    self._process_rect(AvatarSize.S_204x175, resized_image_1, final_path)
                    # proceso las áreas del segundo escalado
                    self._process_rect(AvatarSize.S_136x234, resized_image_2, final_path)
                        
                    faceRect = self.face_detector.detect_face_center_rect_optimized(resized_image_2, (38, 38))
                    if faceRect is not None:
                        self._process_face(faceRect, resized_image_2, final_path)
                        
                    # guardo una copia de la imagen original
                    original_copy_path = os.path.join(final_path, f"original.png")
                    image.save(original_copy_path)
                    
                
    def _remove_background(self, input_image_path: str, output_image_path: str) -> None:
        self.background_remover.remove_background(input_image_path, output_image_path)

    def _resize_image(self, image: Image.Image, width: int, height: int) -> Image.Image:
        return image.resize((width, height), Image.LANCZOS)

    def _process_face(self, faceRect, image: Image.Image, output_dir: str) -> None:
        x, y, w, h = faceRect
        face_image = image.crop((x, y, x + w, y + h))
        os.makedirs(output_dir, exist_ok=True)
        face_image.save(os.path.join(output_dir, f"avatar_{w}x{h}.png"))
        
    def _process_rect(self, areaRect, image: Image.Image, output_dir: str) -> None:
        x, y, w, h = areaRect.value  # Accede al valor del enum antes de desempaquetar
        os.makedirs(output_dir, exist_ok=True)
        self._crop_and_save_areas(image, (x, y, w, h), output_dir)

    def _crop_and_save_areas(self, image: Image.Image, face_coords, output_dir: str) -> None:
        x, y, w, h = face_coords
        face_image = image.crop((x, y, x + w, y + h))

        size = (face_coords[2], face_coords[3])
        cropped = face_image.resize(size, Image.LANCZOS)
        cropped.save(os.path.join(output_dir, f"avatar_{size[0]}x{size[1]}.png"))