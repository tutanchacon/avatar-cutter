"""
Ejemplo de uso del BackgroundRemoverFactory
Demuestra cómo cambiar entre diferentes implementaciones de forma flexible.
"""

from src.background_remover_factory import (
    BackgroundRemoverFactory,
    create_tutanchacon_remover,
    create_api_remover,
    create_best_available_remover
)

def demo_factory_usage():
    """Demuestra diferentes formas de usar el factory."""
    
    print("🏭 BackgroundRemoverFactory - Demo")
    print("=" * 45)
    
    # Verificar qué removedores están disponibles
    available = BackgroundRemoverFactory.get_available_types()
    tutanchacon_available = BackgroundRemoverFactory.is_tutanchacon_available()
    
    print(f"📦 Removedores disponibles: {available}")
    print(f"🎨 TutanchaconBgRemover disponible: {'✅' if tutanchacon_available else '❌'}")
    print()
    
    # Ejemplo 1: Usar el mejor disponible
    print("1️⃣ Creando el mejor removedor disponible:")
    try:
        bg_remover = create_best_available_remover()
        print(f"   ✅ Creado: {type(bg_remover).__name__}")
        print(f"   📝 Descripción: {bg_remover}")
    except ValueError as e:
        print(f"   ❌ Error: {e}")
    print()
    
    # Ejemplo 2: Usar específicamente TutanchaconBgRemover
    print("2️⃣ Creando TutanchaconBgRemover con configuración personalizada:")
    tutanchacon_remover = create_tutanchacon_remover(
        min_alpha_threshold=15,  # Más conservador
        preserve_elements=True,
        model_name='isnet-general-use'
    )
    if tutanchacon_remover:
        print(f"   ✅ Creado: {tutanchacon_remover}")
    else:
        print("   ❌ TutanchaconBgRemover no disponible")
        print("   💡 Ejecuta setup_bgremover.bat para instalarlo")
    print()
    
    # Ejemplo 3: Factory con diferentes configuraciones
    print("3️⃣ Factory con configuraciones específicas:")
    
    configs = [
        {
            "name": "Avatar complejo",
            "params": {
                "remover_type": "tutanchacon",
                "min_alpha_threshold": 10,
                "preserve_elements": True,
                "smooth_edges": True
            }
        },
        {
            "name": "Procesamiento rápido",
            "params": {
                "remover_type": "tutanchacon", 
                "model_name": "u2net",
                "min_alpha_threshold": 50,
                "preserve_elements": False
            }
        }
    ]
    
    for config in configs:
        try:
            remover = BackgroundRemoverFactory.create_remover(**config["params"])
            print(f"   ✅ {config['name']}: {type(remover).__name__}")
        except Exception as e:
            print(f"   ❌ {config['name']}: {e}")
    print()

def demo_practical_usage():
    """Ejemplo práctico de uso en una aplicación."""
    
    print("🔧 Uso práctico en aplicación:")
    print("-" * 35)
    
    # Configuración que puede cambiar según necesidades
    USE_TUTANCHACON = True  # Cambiar a False para usar API
    
    print(f"🎯 Configuración: USE_TUTANCHACON = {USE_TUTANCHACON}")
    
    if USE_TUTANCHACON and BackgroundRemoverFactory.is_tutanchacon_available():
        # Usar TutanchaconBgRemover con configuración optimizada
        bg_remover = BackgroundRemoverFactory.create_remover(
            'tutanchacon',
            min_alpha_threshold=20,
            preserve_elements=True
        )
        print(f"✅ Usando TutanchaconBgRemover: {bg_remover}")
        
    else:
        # Fallback a API
        print("⚠️ TutanchaconBgRemover no disponible o no seleccionado")
        print("🔄 Intentando usar RemoveBgService...")
        
        try:
            # En una aplicación real, obtendrías esto de Config
            api_key = "tu_api_key_aqui"  # Config.get_remove_bg_api_key()
            
            if api_key and api_key != "tu_api_key_aqui":
                bg_remover = BackgroundRemoverFactory.create_remover('api', api_key=api_key)
                print(f"✅ Usando RemoveBgService (API)")
            else:
                print("❌ No hay API key configurada")
                return None
                
        except Exception as e:
            print(f"❌ Error configurando API: {e}")
            return None
    
    return bg_remover

def demo_error_handling():
    """Demuestra manejo de errores."""
    
    print("\n🚨 Demostración de manejo de errores:")
    print("-" * 45)
    
    # Error: tipo inválido
    try:
        BackgroundRemoverFactory.create_remover('invalid_type')
    except ValueError as e:
        print(f"✅ Error detectado correctamente: {e}")
    
    # Error: API sin key
    try:
        BackgroundRemoverFactory.create_remover('api')
    except ValueError as e:
        print(f"✅ Error de API key detectado: {e}")

def main():
    """Función principal del demo."""
    
    demo_factory_usage()
    
    bg_remover = demo_practical_usage()
    
    if bg_remover:
        print(f"\n🎉 Removedor configurado exitosamente!")
        print(f"🔧 Tipo: {type(bg_remover).__name__}")
        print(f"📝 Listo para usar:")
        print(f"    bg_remover.remove_background('input.jpg', 'output.png')")
    
    demo_error_handling()
    
    print(f"\n💡 Consejos:")
    print(f"   - Usa create_best_available_remover() para automático")
    print(f"   - Usa el factory para control completo")
    print(f"   - TutanchaconBgRemover ofrece mejor calidad")
    print(f"   - RemoveBgService como fallback confiable")

if __name__ == "__main__":
    main()
