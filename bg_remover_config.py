"""
Configuración centralizada para el removedor de fondos.
Cambiar estos valores para elegir qué implementación usar.
"""

class BackgroundRemoverConfig:
    """Configuración para el removedor de fondos."""
    
    # ========================================
    # CONFIGURACIÓN PRINCIPAL
    # ========================================
    
    # Tipo de removedor a usar: 'tutanchacon' o 'api'
    REMOVER_TYPE = 'tutanchacon'
    
    # ========================================
    # CONFIGURACIÓN TUTANCHACON BG REMOVER
    # ========================================
    
    # Modelo de IA a usar
    TUTANCHACON_MODEL = 'isnet-general-use'  # 'isnet-general-use', 'u2net', 'u2net_human_seg', 'silueta'
    
    # Umbral de transparencia (0-255)
    # 10-15: Muy conservador, preserva casi todo
    # 20: Configuración óptima para avatares (RECOMENDADO)
    # 50: Configuración balanceada
    # 100+: Más agresivo, remueve más elementos
    TUTANCHACON_ALPHA_THRESHOLD = 20
    
    # Preservar elementos del personaje (accesorios, props, etc.)
    TUTANCHACON_PRESERVE_ELEMENTS = True
    
    # Suavizar bordes
    TUTANCHACON_SMOOTH_EDGES = True
    
    # ========================================
    # PRESETS PREDEFINIDOS
    # ========================================
    
    PRESETS = {
        'avatar_calidad_maxima': {
            'model_name': 'isnet-general-use',
            'min_alpha_threshold': 15,
            'preserve_elements': True,
            'smooth_edges': True
        },
        
        'avatar_equilibrado': {
            'model_name': 'isnet-general-use', 
            'min_alpha_threshold': 20,
            'preserve_elements': True,
            'smooth_edges': True
        },
        
        'procesamiento_rapido': {
            'model_name': 'u2net',
            'min_alpha_threshold': 50,
            'preserve_elements': False,
            'smooth_edges': False
        },
        
        'avatar_complejo': {
            'model_name': 'isnet-general-use',
            'min_alpha_threshold': 10,
            'preserve_elements': True,
            'smooth_edges': True
        }
    }
    
    # Preset activo (usar None para configuración manual)
    ACTIVE_PRESET = 'avatar_equilibrado'  # None, 'avatar_calidad_maxima', 'avatar_equilibrado', etc.
    
    @classmethod
    def get_tutanchacon_config(cls):
        """Obtiene la configuración para TutanchaconBgRemover."""
        if cls.ACTIVE_PRESET and cls.ACTIVE_PRESET in cls.PRESETS:
            return cls.PRESETS[cls.ACTIVE_PRESET]
        else:
            return {
                'model_name': cls.TUTANCHACON_MODEL,
                'min_alpha_threshold': cls.TUTANCHACON_ALPHA_THRESHOLD,
                'preserve_elements': cls.TUTANCHACON_PRESERVE_ELEMENTS,
                'smooth_edges': cls.TUTANCHACON_SMOOTH_EDGES
            }
    
    @classmethod
    def get_available_presets(cls):
        """Retorna los presets disponibles."""
        return list(cls.PRESETS.keys())
    
    @classmethod
    def set_preset(cls, preset_name):
        """Cambia el preset activo."""
        if preset_name in cls.PRESETS:
            cls.ACTIVE_PRESET = preset_name
        else:
            raise ValueError(f"Preset no válido: {preset_name}. Disponibles: {cls.get_available_presets()}")
    
    @classmethod  
    def print_current_config(cls):
        """Imprime la configuración actual."""
        print("🔧 Configuración actual del removedor de fondos:")
        print("=" * 50)
        print(f"Tipo: {cls.REMOVER_TYPE}")
        
        if cls.REMOVER_TYPE == 'tutanchacon':
            config = cls.get_tutanchacon_config()
            preset_info = f" (preset: {cls.ACTIVE_PRESET})" if cls.ACTIVE_PRESET else " (manual)"
            print(f"Configuración TutanchaconBgRemover{preset_info}:")
            for key, value in config.items():
                print(f"  {key}: {value}")
        
        print("=" * 50)
