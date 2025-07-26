"""
Implementación de BackgroundRemover usando el repositorio bgremover de tutanchacon.
https://github.com/tutanchacon/bgremover
"""

import os
import sys
from typing import Optional
from .background_remover import BackgroundRemover


class TutanchaconBgRemover(BackgroundRemover):
    """
    Implementación de BackgroundRemover que utiliza el repositorio bgremover
    de tutanchacon para remover fondos con alta calidad y preservación de elementos.
    
    Características:
    - Preservación de elementos del personaje (accesorios, props, etc.)
    - Corrección de transparencias parciales  
    - Calidad profesional con modelo ISNet
    - Configuración optimizada para avatares
    """
    
    def __init__(self, 
                 model_name: str = 'isnet-general-use',
                 min_alpha_threshold: int = 20,
                 preserve_elements: bool = True,
                 smooth_edges: bool = True):
        """
        Inicializa el removedor de fondos.
        
        Args:
            model_name: Modelo de rembg a utilizar (default: 'isnet-general-use')
            min_alpha_threshold: Umbral mínimo de transparencia para preservar elementos (0-255)
            preserve_elements: Si preservar elementos del personaje
            smooth_edges: Si aplicar suavizado de bordes
        """
        self.model_name = model_name
        self.min_alpha_threshold = min_alpha_threshold
        self.preserve_elements = preserve_elements
        self.smooth_edges = smooth_edges
        self._bg_remover = None
        self._initialize_bg_remover()
    
    def _initialize_bg_remover(self):
        """Inicializa el removedor de fondos de bgremover."""
        try:
            # Intentar importar el paquete bgremover_package
            from bgremover_package import BackgroundRemover as BgRemoverPackage
            self._bg_remover = BgRemoverPackage(model_name=self.model_name)
            self._use_package = True
            print(f"✅ Inicializado bgremover_package con modelo {self.model_name}")
            
        except ImportError:
            try:
                # Si no está disponible el paquete, intentar la versión standalone
                from bgremover_standalone import BackgroundRemoverStandalone
                self._bg_remover = BackgroundRemoverStandalone(model_name=self.model_name)
                self._use_package = False
                print(f"✅ Inicializado bgremover_standalone con modelo {self.model_name}")
                
            except ImportError:
                try:
                    # Como último recurso, intentar importar las funciones del script original
                    from bgremover import remove_background_preserve_elements
                    self._bg_remover = remove_background_preserve_elements
                    self._use_package = None
                    print(f"✅ Inicializado bgremover script original")
                    
                except ImportError:
                    raise ImportError(
                        "No se pudo importar bgremover. Asegúrate de que el repositorio "
                        "https://github.com/tutanchacon/bgremover esté disponible. "
                        "Opciones:\n"
                        "1. Instalar como paquete: pip install -e .\n"
                        "2. Copiar bgremover_standalone.py al proyecto\n"
                        "3. Copiar bgremover.py al proyecto\n"
                        "4. Agregar el repositorio al PYTHONPATH"
                    )
    
    def remove_background(self, input_path: str, output_path: str) -> None:
        """
        Remueve el fondo de una imagen usando bgremover de tutanchacon.
        
        Args:
            input_path: Ruta de la imagen de entrada
            output_path: Ruta donde guardar la imagen sin fondo
            
        Raises:
            FileNotFoundError: Si la imagen de entrada no existe
            Exception: Si hay error en el procesamiento
        """
        # Validar que el archivo de entrada existe
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"La imagen de entrada no existe: {input_path}")
        
        # Crear directorio de salida si no existe
        output_dir = os.path.dirname(output_path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir, exist_ok=True)
        
        try:
            if self._use_package is True:
                # Usar bgremover_package (versión completa)
                success = self._bg_remover.remove_background(
                    input_path=input_path,
                    output_path=output_path,
                    min_alpha_threshold=self.min_alpha_threshold,
                    preserve_elements=self.preserve_elements,
                    smooth_edges=self.smooth_edges,
                    verbose=True
                )
                
                if not success:
                    raise Exception("Error en el procesamiento con bgremover_package")
                    
            elif self._use_package is False:
                # Usar bgremover_standalone
                success = self._bg_remover.process(
                    input_path=input_path,
                    output_path=output_path,
                    threshold=self.min_alpha_threshold,
                    verbose=True
                )
                
                if not success:
                    raise Exception("Error en el procesamiento con bgremover_standalone")
                    
            else:
                # Usar script original bgremover.py
                self._bg_remover(
                    input_path=input_path,
                    output_path=output_path,
                    min_alpha_threshold=self.min_alpha_threshold,
                    verbose=True
                )
            
            print(f"✅ Fondo removido exitosamente: {output_path}")
            
        except Exception as e:
            error_msg = f"Error al remover el fondo de {input_path}: {str(e)}"
            print(f"❌ {error_msg}")
            raise Exception(error_msg)
    
    def get_stats(self, image_path: str) -> Optional[dict]:
        """
        Obtiene estadísticas de una imagen si está disponible en bgremover.
        
        Args:
            image_path: Ruta de la imagen
            
        Returns:
            dict: Estadísticas de la imagen o None si no está disponible
        """
        if self._use_package is True and hasattr(self._bg_remover, 'get_stats'):
            try:
                return self._bg_remover.get_stats(image_path)
            except Exception as e:
                print(f"⚠️ Error obteniendo estadísticas: {e}")
                return None
        
        print("ℹ️ Estadísticas no disponibles en esta versión de bgremover")
        return None
    
    def set_threshold(self, threshold: int):
        """
        Actualiza el umbral de transparencia.
        
        Args:
            threshold: Nuevo umbral (0-255)
        """
        if 0 <= threshold <= 255:
            self.min_alpha_threshold = threshold
            print(f"🎯 Umbral actualizado a: {threshold}")
        else:
            raise ValueError("El umbral debe estar entre 0 y 255")
    
    def set_model(self, model_name: str):
        """
        Cambia el modelo de IA para remover fondos.
        
        Args:
            model_name: Nombre del modelo ('isnet-general-use', 'u2net', etc.)
        """
        self.model_name = model_name
        print(f"🔄 Cambiando modelo a: {model_name}")
        self._initialize_bg_remover()
    
    def __str__(self):
        """Representación string de la instancia."""
        version = "package" if self._use_package is True else "standalone" if self._use_package is False else "script"
        return (f"TutanchaconBgRemover(model={self.model_name}, "
                f"threshold={self.min_alpha_threshold}, version={version})")
