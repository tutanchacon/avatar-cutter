# TutanchaconBgRemover - Integración con bgremover

Esta clase implementa la interfaz `BackgroundRemover` utilizando el repositorio de alta calidad [bgremover de tutanchacon](https://github.com/tutanchacon/bgremover).

## 🎯 Características

- **Preservación de elementos**: Mantiene accesorios, props y detalles del personaje
- **Calidad profesional**: Utiliza modelo ISNet para segmentación AI avanzada
- **Configuración optimizada**: Parámetros específicos para avatares
- **Transparencias inteligentes**: Convierte transparencias parciales a completamente opacas
- **Múltiples versiones**: Soporte para paquete completo, standalone o script original

## 🚀 Instalación

### Opción 1: Instalación automática
```bash
# Ejecutar el script de configuración
setup_bgremover.bat
```

### Opción 2: Instalación manual
```bash
# 1. Instalar dependencias
pip install -r bgremover_requirements.txt

# 2. Clonar repositorio
git clone https://github.com/tutanchacon/bgremover.git

# 3. Instalar como paquete
cd bgremover
pip install -e .
```

### Opción 3: Solo dependencias mínimas
```bash
# Copiar bgremover_standalone.py al directorio src/
# Instalar solo rembg
pip install rembg>=2.0.50
```

## 📖 Uso

### Uso básico
```python
from src.tutanchacon_bg_remover import TutanchaconBgRemover

# Crear instancia con configuración optimizada
bg_remover = TutanchaconBgRemover(
    model_name='isnet-general-use',  # Modelo más preciso
    min_alpha_threshold=20,          # Configuración óptima recomendada
    preserve_elements=True,          # Preservar elementos del personaje
    smooth_edges=True               # Suavizar bordes
)

# Remover fondo
bg_remover.remove_background('input.jpg', 'output.png')
```

### Configuración avanzada
```python
# Para avatares complejos con muchos detalles
bg_remover = TutanchaconBgRemover(
    model_name='isnet-general-use',
    min_alpha_threshold=10,    # Más conservador
    preserve_elements=True,
    smooth_edges=True
)

# Para procesamiento rápido
bg_remover = TutanchaconBgRemover(
    model_name='u2net',
    min_alpha_threshold=50,    # Menos conservador
    preserve_elements=False,
    smooth_edges=False
)
```

### Usando con la interfaz común
```python
from src.tutanchacon_bg_remover import TutanchaconBgRemover

# Implementa BackgroundRemover, se puede usar en cualquier lugar
def process_avatar(bg_remover_instance):
    bg_remover_instance.remove_background('input.jpg', 'output.png')

# Usar con TutanchaconBgRemover
tutanchacon_remover = TutanchaconBgRemover()
process_avatar(tutanchacon_remover)
```

## 🎨 Modelos disponibles

- **isnet-general-use** (recomendado): Mejor calidad general, preserva detalles
- **u2net**: Más rápido, buena calidad
- **u2net_human_seg**: Optimizado para segmentación humana
- **silueta**: Bueno para personas/avatares

## 🔧 Parámetros de configuración

### min_alpha_threshold
- **10-15**: Muy conservador, preserva casi todo
- **20** (recomendado): Configuración óptima para avatares
- **50**: Configuración balanceada
- **100+**: Más agresivo, remueve más elementos

### preserve_elements
- **True**: Preserva accesorios, props, elementos del personaje
- **False**: Procesamiento más rápido, menos preservación

### smooth_edges
- **True**: Aplica suavizado conservador de bordes
- **False**: Bordes más duros, procesamiento más rápido

## 🎯 Casos de uso

### Para avatares de videojuegos
```python
# Configuración para preservar armas, accesorios, efectos
bg_remover = TutanchaconBgRemover(
    min_alpha_threshold=15,
    preserve_elements=True,
    smooth_edges=True
)
```

### Para fotos de perfil
```python
# Configuración balanceada para fotos personales
bg_remover = TutanchaconBgRemover(
    min_alpha_threshold=20,
    preserve_elements=True,
    smooth_edges=True
)
```

### Para procesamiento masivo
```python
# Configuración optimizada para velocidad
bg_remover = TutanchaconBgRemover(
    model_name='u2net',
    min_alpha_threshold=50,
    preserve_elements=False,
    smooth_edges=False
)
```

## 🚨 Solución de problemas

### Error de importación
```
ImportError: No se pudo importar bgremover
```
**Solución**: Ejecutar `setup_bgremover.bat` o instalar manualmente las dependencias.

### Calidad insuficiente
- Reducir `min_alpha_threshold` a 10-15
- Asegurarse de que `preserve_elements=True`
- Probar con modelo `isnet-general-use`

### Elementos deseados removidos
- Reducir `min_alpha_threshold`
- Activar `preserve_elements=True`
- Considerar usar `smooth_edges=False` para bordes más duros

### Procesamiento lento
- Cambiar a modelo `u2net`
- Usar `preserve_elements=False`
- Usar `smooth_edges=False`

## 📊 Comparación con otros métodos

| Aspecto | TutanchaconBgRemover | Métodos básicos |
|---------|---------------------|-----------------|
| Calidad | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Preservación de elementos | ⭐⭐⭐⭐⭐ | ⭐⭐ |
| Velocidad | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Configurabilidad | ⭐⭐⭐⭐⭐ | ⭐⭐ |

## 🔗 Referencias

- [Repositorio bgremover](https://github.com/tutanchacon/bgremover)
- [Documentación rembg](https://github.com/danielgatis/rembg)
- [Modelo ISNet](https://github.com/xuebinqin/DIS)
