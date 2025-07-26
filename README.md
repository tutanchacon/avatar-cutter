# Avatar Image Processor

Sistema de procesamiento de imágenes de avatar que incluye detección facial, remoción de fondo y redimensionado automático a múltiples tamaños estándar.

## Características

- **Remoción de fondo**: Utiliza la API de remove.bg para eliminar fondos de imágenes
- **Detección facial**: Detección automática de rostros usando OpenCV
- **Redimensionado inteligente**: Redimensiona imágenes manteniendo proporciones
- **Múltiples tamaños**: Genera avatares en diferentes tamaños (38x38, 86x86, 136x234, 204x175, 204x350)
- **Procesamiento por lotes**: Procesa múltiples imágenes automáticamente

## Estructura del Proyecto

```
avatarImageProcessor/
├── src/                          # Código fuente principal
│   ├── avatar_size.py           # Definición de tamaños de avatar
│   ├── background_remover.py    # Interfaz abstracta para remoción de fondo
│   ├── face_detector.py         # Detector de rostros con OpenCV
│   ├── image_processor.py       # Procesador principal de imágenes
│   ├── image_resizer.py         # Interfaz abstracta para redimensionado
│   ├── proportional_image_resizer.py  # Redimensionador proporcional
│   └── remove_bg_service.py     # Servicio de remoción de fondo
├── model/                       # Modelos de ML (Haar Cascades)
│   ├── deploy.prototxt
│   └── res10_300x300_ssd_iter_140000_fp16.caffemodel
├── p1_rawimages/               # Imágenes originales
├── p2_approvedimages/          # Imágenes aprobadas
├── p3_bgremoved/               # Imágenes sin fondo
├── p4_croppedimages/           # Imágenes procesadas finales
├── remove_bg.py                # Script para remoción de fondo
├── resize_images.py            # Script para redimensionado
├── requirements.txt            # Dependencias del proyecto
└── setup.py                    # Configuración de instalación
```

## Requisitos del Sistema

- Python 3.8 o superior
- Sistema operativo: Windows, macOS, Linux
- Acceso a internet (para API de remove.bg)

## Instalación

### Método 1: Instalación Automática (Recomendado)

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd avatarImageProcessor
```

2. **Ejecutar el instalador automático**
```bash
python install.py
```

3. **Configurar API Key**
Edita el archivo `.env` y configura tu API key de remove.bg:
```
REMOVE_BG_API_KEY=tu_api_key_aqui
```

4. **Verificar instalación**
```bash
python check_system.py
```

### Método 2: Instalación Manual

1. **Clonar el repositorio**
```bash
git clone <repository-url>
cd avatarImageProcessor
```

2. **Crear entorno virtual**
```bash
python -m venv avatarprocess_env
```

3. **Activar el entorno virtual**

**Windows:**
```bash
avatarprocess_env\Scripts\activate
```

**macOS/Linux:**
```bash
source avatarprocess_env/bin/activate
```

4. **Instalar dependencias**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

5. **Configurar variables de entorno**
```bash
cp .env.example .env
# Editar .env y configurar tu API key
```

6. **Crear directorios necesarios**
```bash
mkdir p1_rawimages p2_approvedimages p3_bgremoved p4_croppedimages
```

### Instalación como Paquete Python

Para instalar el proyecto como un paquete Python:

```bash
# Modo desarrollo (cambios se reflejan inmediatamente)
pip install -e .

# Instalación estándar
pip install .
```

## Configuración

### Configuración de API Key

El proyecto utiliza la API de remove.bg para eliminar fondos de imágenes. Para configurarla:

1. **Obtener API Key**
   - Regístrate en [remove.bg](https://www.remove.bg/api)
   - Obtén tu API key gratuita

2. **Configurar mediante archivo .env** (Recomendado)
   ```bash
   # Copia el archivo de ejemplo
   cp .env.example .env
   
   # Edita .env y configura tu API key
   REMOVE_BG_API_KEY=tu_api_key_aqui
   ```

3. **Configurar mediante variable de entorno**
   ```bash
   # Windows
   set REMOVE_BG_API_KEY=tu_api_key_aqui
   
   # macOS/Linux
   export REMOVE_BG_API_KEY=tu_api_key_aqui
   ```

### Verificación de la Configuración

Ejecuta el verificador del sistema para asegurar que todo esté configurado correctamente:

```bash
python check_system.py
```

Este script verificará:
- ✅ Versión de Python compatible
- ✅ Entorno virtual activo
- ✅ Dependencias instaladas
- ✅ API key configurada
- ✅ Directorios necesarios
- ✅ Archivos del modelo disponibles

## Uso

### Remoción de Fondo
```bash
python remove_bg.py
```

### Redimensionado y Procesamiento Completo
```bash
python resize_images.py
```

### Uso Programático
```python
from src.remove_bg_service import RemoveBgService
from src.proportional_image_resizer import ProportionalImageResizer
from src.face_detector import FaceDetector
from src.image_processor import ImageProcessor
import cv2

# Configurar servicios
background_remover = RemoveBgService(api_key='tu_api_key')
image_resizer = ProportionalImageResizer()
face_detector = FaceDetector(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Procesar imágenes
processor = ImageProcessor(background_remover, image_resizer, face_detector)
processor.resize_images('input_directory', 'output_directory')
```

## Dependencias Principales

- **OpenCV (cv2)**: Procesamiento de imágenes y detección facial
- **Pillow (PIL)**: Manipulación de imágenes
- **NumPy**: Operaciones numéricas
- **Requests**: Comunicación con API de remove.bg
- **Matplotlib**: Visualización (opcional)

## Flujo de Trabajo

1. **Entrada**: Imágenes en formato PNG/JPG en `p1_rawimages/` o `p2_approvedimages/`
2. **Remoción de fondo**: Se eliminan los fondos usando remove.bg API
3. **Detección facial**: Se detecta y localiza el rostro principal
4. **Redimensionado**: Se generan múltiples tamaños manteniendo proporciones
5. **Salida**: Imágenes procesadas en `p3_bgremoved/` y `p4_croppedimages/`

## Tamaños de Avatar Generados

- **38x38**: Avatar pequeño para iconos
- **86x86**: Avatar mediano
- **136x234**: Avatar vertical
- **204x175**: Avatar horizontal
- **204x350**: Avatar grande vertical

## Solución de Problemas

### Error de codificación UTF-8
Si encuentras errores de codificación, asegúrate de que todos los archivos Python estén guardados en UTF-8.

### Error de API Key
Verifica que tu API key de remove.bg sea válida y que tengas créditos disponibles.

### Error de OpenCV
Asegúrate de que los modelos de Haar Cascades estén disponibles:
```python
import cv2
print(cv2.data.haarcascades)
```

## Desarrollo

### Estructura del Código

El proyecto sigue principios de programación orientada a objetos:

- **Interfaces abstractas**: `BackgroundRemover`, `ImageResizer`
- **Implementaciones concretas**: `RemoveBgService`, `ProportionalImageResizer`
- **Composición**: `ImageProcessor` utiliza todos los servicios

### Extensibilidad

Puedes agregar nuevos procesadores implementando las interfaces abstractas:

```python
from src.background_remover import BackgroundRemover

class MiNuevoRemovedor(BackgroundRemover):
    def remove_background(self, input_path: str, output_path: str) -> None:
        # Tu implementación aquí
        pass
```

## Licencia

MIT License - Ver archivo LICENSE para más detalles.

## Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -am 'Agregar nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Crea un Pull Request
