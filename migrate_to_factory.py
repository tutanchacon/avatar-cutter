"""
Script de migración para cambiar entre RemoveBgService y TutanchaconBgRemover
Permite elegir qué implementación usar para remover fondos.
"""

import os
import sys
from pathlib import Path

def create_bg_remover_factory():
    """Crea un factory pattern para elegir el removedor de fondos."""
    
    factory_content = '''"""
Factory para crear instancias de removedores de fondo.
Permite cambiar fácilmente entre diferentes implementaciones.
"""

from typing import Union, Optional
from .background_remover import BackgroundRemover
from .remove_bg_service import RemoveBgService

# Importar TutanchaconBgRemover solo si está disponible
try:
    from .tutanchacon_bg_remover import TutanchaconBgRemover
    TUTANCHACON_AVAILABLE = True
except ImportError:
    TUTANCHACON_AVAILABLE = False
    TutanchaconBgRemover = None

class BackgroundRemoverFactory:
    """
    Factory para crear removedores de fondo.
    
    Soporta:
    - 'api': RemoveBgService (requiere API key)
    - 'tutanchacon': TutanchaconBgRemover (requiere bgremover instalado)
    """
    
    @staticmethod
    def create_remover(
        remover_type: str = 'tutanchacon',
        api_key: Optional[str] = None,
        **kwargs
    ) -> BackgroundRemover:
        """
        Crea una instancia del removedor de fondo especificado.
        
        Args:
            remover_type: Tipo de removedor ('api' o 'tutanchacon')
            api_key: API key para RemoveBgService (requerida para type='api')
            **kwargs: Argumentos adicionales para el removedor
            
        Returns:
            BackgroundRemover: Instancia del removedor
            
        Raises:
            ValueError: Si el tipo no es válido o faltan parámetros
            ImportError: Si el removedor solicitado no está disponible
        """
        
        if remover_type == 'api':
            if api_key is None:
                raise ValueError("API key es requerida para RemoveBgService")
            return RemoveBgService(api_key=api_key)
            
        elif remover_type == 'tutanchacon':
            if not TUTANCHACON_AVAILABLE:
                raise ImportError(
                    "TutanchaconBgRemover no está disponible. "
                    "Ejecuta setup_bgremover.bat para instalarlo."
                )
            
            # Configuración por defecto optimizada para avatares
            default_config = {
                'model_name': 'isnet-general-use',
                'min_alpha_threshold': 20,
                'preserve_elements': True,
                'smooth_edges': True
            }
            
            # Combinar configuración por defecto con kwargs
            config = {**default_config, **kwargs}
            return TutanchaconBgRemover(**config)
            
        else:
            available_types = ['api']
            if TUTANCHACON_AVAILABLE:
                available_types.append('tutanchacon')
                
            raise ValueError(
                f"Tipo de removedor no válido: {remover_type}. "
                f"Tipos disponibles: {available_types}"
            )
    
    @staticmethod
    def get_available_types() -> list:
        """Retorna los tipos de removedores disponibles."""
        types = ['api']
        if TUTANCHACON_AVAILABLE:
            types.append('tutanchacon')
        return types
    
    @staticmethod
    def is_tutanchacon_available() -> bool:
        """Verifica si TutanchaconBgRemover está disponible."""
        return TUTANCHACON_AVAILABLE

# Funciones de conveniencia
def create_api_remover(api_key: str) -> RemoveBgService:
    """Crea un removedor usando la API de remove.bg"""
    return BackgroundRemoverFactory.create_remover('api', api_key=api_key)

def create_tutanchacon_remover(**kwargs) -> Union[TutanchaconBgRemover, None]:
    """Crea un removedor usando bgremover de tutanchacon"""
    try:
        return BackgroundRemoverFactory.create_remover('tutanchacon', **kwargs)
    except ImportError:
        return None

def create_best_available_remover(api_key: Optional[str] = None, **kwargs) -> BackgroundRemover:
    """
    Crea el mejor removedor disponible.
    Prioriza TutanchaconBgRemover, pero usa API si no está disponible.
    """
    if TUTANCHACON_AVAILABLE:
        return create_tutanchacon_remover(**kwargs)
    elif api_key:
        return create_api_remover(api_key)
    else:
        raise ValueError(
            "No hay removedores disponibles. "
            "Instala bgremover o proporciona una API key."
        )
'''
    
    with open('src/background_remover_factory.py', 'w', encoding='utf-8') as f:
        f.write(factory_content)
    
    print("✅ Factory creado: src/background_remover_factory.py")

def update_files_to_use_factory():
    """Actualiza los archivos principales para usar el factory."""
    
    files_to_update = [
        {
            'file': 'resize_images.py',
            'old_import': 'from src.tutanchacon_bg_remover import TutanchaconBgRemover',
            'new_import': 'from src.background_remover_factory import create_best_available_remover',
            'old_creation': '''    # Usar TutanchaconBgRemover con configuración optimizada para avatares
    background_remover = TutanchaconBgRemover(
        model_name='isnet-general-use',  # Modelo más preciso
        min_alpha_threshold=20,          # Configuración óptima para avatares
        preserve_elements=True,          # Preservar accesorios y elementos
        smooth_edges=True               # Suavizar bordes
    )''',
            'new_creation': '''    # Crear el mejor removedor disponible (prioriza TutanchaconBgRemover)
    try:
        background_remover = create_best_available_remover()
    except ValueError:
        # Fallback a API si está configurada
        api_key = Config.get_remove_bg_api_key()
        background_remover = create_best_available_remover(api_key=api_key)'''
        },
        {
            'file': 'remove_bg.py',
            'old_import': 'from src.tutanchacon_bg_remover import TutanchaconBgRemover',
            'new_import': 'from src.background_remover_factory import create_best_available_remover',
            'old_creation': '''    # Usar TutanchaconBgRemover con configuración optimizada para avatares
    background_remover = TutanchaconBgRemover(
        model_name='isnet-general-use',  # Modelo más preciso
        min_alpha_threshold=20,          # Configuración óptima para avatares
        preserve_elements=True,          # Preservar accesorios y elementos
        smooth_edges=True               # Suavizar bordes
    )''',
            'new_creation': '''    # Crear el mejor removedor disponible (prioriza TutanchaconBgRemover)
    try:
        background_remover = create_best_available_remover()
    except ValueError:
        # Fallback a API si está configurada
        api_key = Config.get_remove_bg_api_key()
        background_remover = create_best_available_remover(api_key=api_key)'''
        }
    ]
    
    for file_info in files_to_update:
        file_path = file_info['file']
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Actualizar import
            content = content.replace(file_info['old_import'], file_info['new_import'])
            
            # Actualizar creación del objeto
            content = content.replace(file_info['old_creation'], file_info['new_creation'])
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"✅ Actualizado: {file_path}")

def create_example_usage():
    """Crea un ejemplo de uso del factory."""
    
    example_content = '''"""
Ejemplo de uso del BackgroundRemoverFactory
"""

from src.background_remover_factory import (
    BackgroundRemoverFactory,
    create_tutanchacon_remover,
    create_api_remover,
    create_best_available_remover
)
from config import Config

def example_factory_usage():
    """Demuestra diferentes formas de usar el factory."""
    
    print("🏭 Ejemplo de BackgroundRemoverFactory")
    print("=" * 40)
    
    # Verificar qué removedores están disponibles
    available = BackgroundRemoverFactory.get_available_types()
    print(f"📦 Removedores disponibles: {available}")
    
    # Ejemplo 1: Usar el mejor disponible
    print("\\n1️⃣ Usando el mejor removedor disponible:")
    try:
        bg_remover = create_best_available_remover()
        print(f"✅ Creado: {type(bg_remover).__name__}")
    except ValueError as e:
        print(f"❌ Error: {e}")
    
    # Ejemplo 2: Usar específicamente TutanchaconBgRemover
    print("\\n2️⃣ Usando TutanchaconBgRemover específicamente:")
    tutanchacon_remover = create_tutanchacon_remover(
        min_alpha_threshold=15,  # Más conservador
        preserve_elements=True
    )
    if tutanchacon_remover:
        print(f"✅ Creado: {tutanchacon_remover}")
    else:
        print("❌ TutanchaconBgRemover no disponible")
    
    # Ejemplo 3: Usar API como fallback
    print("\\n3️⃣ Usando API como fallback:")
    try:
        api_key = Config.get_remove_bg_api_key()
        if api_key:
            api_remover = create_api_remover(api_key)
            print(f"✅ API remover creado")
        else:
            print("⚠️ No hay API key configurada")
    except Exception as e:
        print(f"❌ Error con API: {e}")
    
    # Ejemplo 4: Factory con parámetros específicos
    print("\\n4️⃣ Factory con configuración específica:")
    try:
        custom_remover = BackgroundRemoverFactory.create_remover(
            'tutanchacon',
            model_name='u2net',
            min_alpha_threshold=30,
            preserve_elements=False
        )
        print(f"✅ Removedor personalizado: {custom_remover}")
    except Exception as e:
        print(f"❌ Error: {e}")

def example_in_application():
    """Ejemplo de uso en una aplicación real."""
    
    print("\\n🔧 Ejemplo en aplicación:")
    print("-" * 30)
    
    # Configuración flexible
    USE_TUTANCHACON = True  # Cambiar a False para usar API
    
    if USE_TUTANCHACON and BackgroundRemoverFactory.is_tutanchacon_available():
        bg_remover = BackgroundRemoverFactory.create_remover('tutanchacon')
        print("🎨 Usando TutanchaconBgRemover")
    else:
        api_key = Config.get_remove_bg_api_key()
        if api_key:
            bg_remover = BackgroundRemoverFactory.create_remover('api', api_key=api_key)
            print("🌐 Usando RemoveBgService (API)")
        else:
            print("❌ No hay removedor disponible")
            return
    
    # Usar el removedor (ejemplo)
    try:
        # bg_remover.remove_background('input.jpg', 'output.png')
        print(f"✅ Removedor listo: {type(bg_remover).__name__}")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    example_factory_usage()
    example_in_application()
'''
    
    with open('example_factory_usage.py', 'w', encoding='utf-8') as f:
        f.write(example_content)
    
    print("✅ Ejemplo creado: example_factory_usage.py")

def main():
    """Función principal de migración."""
    
    print("🔄 Migración a Factory Pattern")
    print("=" * 40)
    
    # Crear factory
    create_bg_remover_factory()
    
    # Crear ejemplo
    create_example_usage()
    
    print("\\n✅ Migración completada!")
    print("\\n📋 Archivos creados:")
    print("   - src/background_remover_factory.py")
    print("   - example_factory_usage.py")
    
    print("\\n💡 Próximos pasos:")
    print("   1. Revisar el factory creado")
    print("   2. Probar con: python example_factory_usage.py")
    print("   3. Actualizar tus archivos para usar el factory")
    
    # Preguntar si actualizar archivos automáticamente
    print("\\n❓ ¿Actualizar automáticamente resize_images.py y remove_bg.py?")
    print("   Esto los cambiará para usar el factory en lugar de implementaciones específicas")
    
    response = input("Actualizar archivos? (s/n): ").lower().strip()
    
    if response in ['s', 'si', 'y', 'yes']:
        update_files_to_use_factory()
        print("\\n✅ Archivos actualizados para usar factory!")
    else:
        print("\\n⏭️ Archivos no modificados. Puedes actualizarlos manualmente más tarde.")

if __name__ == "__main__":
    main()
