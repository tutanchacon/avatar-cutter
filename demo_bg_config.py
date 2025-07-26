"""
Ejemplo de cómo cambiar la configuración del removedor de fondos.
Demuestra diferentes formas de configurar qué implementación usar.
"""

from bg_remover_config import BackgroundRemoverConfig
from src.background_remover_factory import BackgroundRemoverFactory

def demo_configuration_options():
    """Demuestra diferentes opciones de configuración."""
    
    print("⚙️ Configuración del Removedor de Fondos")
    print("=" * 50)
    
    # Mostrar configuración actual
    print("📋 Configuración actual:")
    BackgroundRemoverConfig.print_current_config()
    
    # Mostrar presets disponibles
    print(f"\n🎨 Presets disponibles:")
    presets = BackgroundRemoverConfig.get_available_presets()
    for i, preset in enumerate(presets, 1):
        config = BackgroundRemoverConfig.PRESETS[preset]
        print(f"  {i}. {preset}:")
        for key, value in config.items():
            print(f"     {key}: {value}")
        print()

def demo_change_to_tutanchacon():
    """Demuestra cómo cambiar a TutanchaconBgRemover."""
    
    print("🎨 Cambiando a TutanchaconBgRemover")
    print("-" * 40)
    
    # Cambiar tipo de removedor
    BackgroundRemoverConfig.REMOVER_TYPE = 'tutanchacon'
    
    # Cambiar preset
    BackgroundRemoverConfig.set_preset('avatar_calidad_maxima')
    
    print("✅ Configuración actualizada:")
    BackgroundRemoverConfig.print_current_config()
    
    # Crear removedor con nueva configuración
    try:
        config = BackgroundRemoverConfig.get_tutanchacon_config()
        bg_remover = BackgroundRemoverFactory.create_remover(
            remover_type='tutanchacon',
            **config
        )
        print(f"✅ Removedor creado: {bg_remover}")
        return bg_remover
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def demo_change_to_api():
    """Demuestra cómo cambiar a RemoveBgService (API)."""
    
    print("\n🌐 Cambiando a RemoveBgService (API)")
    print("-" * 40)
    
    # Cambiar tipo de removedor
    BackgroundRemoverConfig.REMOVER_TYPE = 'api'
    
    print("✅ Configuración actualizada:")
    BackgroundRemoverConfig.print_current_config()
    
    # Crear removedor con nueva configuración (simulado)
    try:
        # En uso real, necesitarías: api_key = Config.get_remove_bg_api_key()
        api_key = "tu_api_key_aqui"
        
        if api_key != "tu_api_key_aqui":
            bg_remover = BackgroundRemoverFactory.create_remover(
                remover_type='api',
                api_key=api_key
            )
            print(f"✅ Removedor API creado")
            return bg_remover
        else:
            print("⚠️ API key no configurada (esto es normal en el demo)")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def demo_custom_configuration():
    """Demuestra configuración personalizada."""
    
    print("\n🔧 Configuración personalizada")
    print("-" * 35)
    
    # Configuración manual (sin preset)
    BackgroundRemoverConfig.REMOVER_TYPE = 'tutanchacon'
    BackgroundRemoverConfig.ACTIVE_PRESET = None  # Usar configuración manual
    BackgroundRemoverConfig.TUTANCHACON_MODEL = 'u2net'
    BackgroundRemoverConfig.TUTANCHACON_ALPHA_THRESHOLD = 30
    BackgroundRemoverConfig.TUTANCHACON_PRESERVE_ELEMENTS = False
    BackgroundRemoverConfig.TUTANCHACON_SMOOTH_EDGES = False
    
    print("✅ Configuración personalizada:")
    BackgroundRemoverConfig.print_current_config()
    
    try:
        config = BackgroundRemoverConfig.get_tutanchacon_config()
        bg_remover = BackgroundRemoverFactory.create_remover(
            remover_type='tutanchacon',
            **config
        )
        print(f"✅ Removedor personalizado: {bg_remover}")
        return bg_remover
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def demo_quick_preset_changes():
    """Demuestra cambios rápidos de presets."""
    
    print("\n⚡ Cambios rápidos de preset")
    print("-" * 35)
    
    # Probar diferentes presets
    test_presets = ['avatar_equilibrado', 'procesamiento_rapido', 'avatar_complejo']
    
    for preset in test_presets:
        print(f"\n🎯 Probando preset: {preset}")
        try:
            BackgroundRemoverConfig.set_preset(preset)
            config = BackgroundRemoverConfig.get_tutanchacon_config()
            
            bg_remover = BackgroundRemoverFactory.create_remover(
                remover_type='tutanchacon',
                **config
            )
            print(f"✅ {preset}: {bg_remover}")
            
        except Exception as e:
            print(f"❌ Error con {preset}: {e}")

def show_usage_instructions():
    """Muestra instrucciones de uso."""
    
    print("\n💡 Cómo cambiar la configuración:")
    print("=" * 45)
    
    print("1️⃣ Editar bg_remover_config.py:")
    print("   - Cambiar REMOVER_TYPE = 'tutanchacon' o 'api'")
    print("   - Cambiar ACTIVE_PRESET para usar presets")
    print("   - O configurar manualmente los parámetros")
    print()
    
    print("2️⃣ Usar presets predefinidos:")
    print("   - 'avatar_calidad_maxima': Máxima calidad")
    print("   - 'avatar_equilibrado': Recomendado general")
    print("   - 'procesamiento_rapido': Para velocidad")
    print("   - 'avatar_complejo': Para avatares detallados")
    print()
    
    print("3️⃣ Programáticamente:")
    print("   BackgroundRemoverConfig.REMOVER_TYPE = 'tutanchacon'")
    print("   BackgroundRemoverConfig.set_preset('avatar_calidad_maxima')")
    print()
    
    print("4️⃣ Los archivos resize_images.py y remove_bg.py")
    print("   usarán automáticamente la configuración elegida.")

def main():
    """Función principal del demo."""
    
    # Configuración inicial
    demo_configuration_options()
    
    # Cambiar a diferentes opciones
    demo_change_to_tutanchacon()
    demo_change_to_api()
    demo_custom_configuration()
    demo_quick_preset_changes()
    
    # Instrucciones
    show_usage_instructions()
    
    print("\n🎉 Demo completado!")
    print("🔧 Edita bg_remover_config.py para cambiar la configuración")

if __name__ == "__main__":
    main()
