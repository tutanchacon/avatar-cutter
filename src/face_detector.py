import cv2
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

class FaceDetector:
    def __init__(self, classifier_path: str):
        self.face_cascade = cv2.CascadeClassifier(classifier_path)

    def detect_face_center_rect(self, cv_image: Image.Image, area_size, search_top_only=True):
        # Cargo el modelo de detección de rostros MobileNet-SSD
        net = cv2.dnn.readNetFromCaffe("./model/deploy.prototxt", "./model/res10_300x300_ssd_iter_140000_fp16.caffemodel")
        
        image = np.array(cv_image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        (h, w) = image.shape[:2]
        
        # Para avatares de cuerpo completo, optimizo buscando solo en la parte superior
        if search_top_only:
            # Recorto la imagen al 40% superior para buscar rostros (donde están las cabezas en avatares)
            search_height = int(h * 0.4)
            search_image = image[:search_height, :]
            search_h = search_height
        else:
            search_image = image
            search_h = h
        
        # Preparo la imagen (o región) para la red
        blob = cv2.dnn.blobFromImage(search_image, 1.0, (300, 300), (104.0, 177.0, 123.0))

        # Paso la imagen por la red para obtener detecciones
        net.setInput(blob)
        detections = net.forward()

        # Dimensiones del área deseada
        width, height = area_size

        # Itero las detecciones
        for i in range(0, detections.shape[2]):
            confidence = detections[0, 0, i, 2]
            # Uso umbral más alto para búsqueda optimizada, más bajo para búsqueda completa
            confidence_threshold = 0.3 if search_top_only else 0.2
            
            if confidence > confidence_threshold:
                box = detections[0, 0, i, 3:7] * np.array([w, search_h, w, search_h])
                (startX, startY, endX, endY) = box.astype("int")

                wSizeHalf = width // 2
                hSizeHalf = height // 2

                # Calculo el centro de la cara
                centerX = (startX + endX) // 2
                centerY = (startY + endY) // 2

                # Si busqué solo en la parte superior, las coordenadas Y ya están correctas
                # porque search_image es una porción de la imagen original

                # Calculo las nuevas coordenadas para un área centrada en la cara
                new_startX = centerX - wSizeHalf
                new_startY = centerY - hSizeHalf

                # Verifico que el rectángulo esté dentro de los límites de la imagen completa
                new_startX = max(0, min(new_startX, w - width))
                new_startY = max(0, min(new_startY, h - height))

                # Creo el rectángulo para el área de la cara
                faceRect = (new_startX, new_startY, width, height)

                return faceRect

        return None
    
    def detect_face_center_rect_optimized(self, cv_image: Image.Image, area_size):
        """
        Versión optimizada para avatares de cuerpo completo.
        Busca primero en la zona superior, luego en toda la imagen si es necesario.
        """
        # Primer intento: buscar solo en el 40% superior (más rápido y preciso para avatares)
        face_rect = self.detect_face_center_rect(cv_image, area_size, search_top_only=True)
        
        if face_rect is not None:
            return face_rect
        
        # Segundo intento: buscar en toda la imagen con umbral más bajo
        print("No se encontró rostro en zona superior, buscando en toda la imagen...")
        return self.detect_face_center_rect(cv_image, area_size, search_top_only=False)