"""
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

def create_tutanchacon_remover(**kwargs):
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
