"""
Script de prueba para TutanchaconBgRemover
Demuestra las diferentes configuraciones y capacidades
"""

import os
import sys
from pathlib import Path

# Agregar el directorio actual al path para imports
sys.path.append(str(Path(__file__).parent))

try:
    from src.tutanchacon_bg_remover import TutanchaconBgRemover
    from src.background_remover import BackgroundRemover
except ImportError as e:
    print(f"❌ Error de importación: {e}")
    print("🔧 Asegúrate de ejecutar setup_bgremover.bat primero")
    sys.exit(1)

def test_basic_usage():
    """Prueba el uso básico del removedor de fondos."""
    print("\n🧪 Prueba 1: Uso básico")
    print("-" * 30)
    
    try:
        # Configuración básica
        bg_remover = TutanchaconBgRemover()
        
        print(f"✅ Instancia creada: {bg_remover}")
        
        # Verificar que implementa la interfaz
        assert isinstance(bg_remover, BackgroundRemover)
        print("✅ Implementa correctamente la interfaz BackgroundRemover")
        
        return bg_remover
        
    except Exception as e:
        print(f"❌ Error en prueba básica: {e}")
        return None

def test_configuration_options():
    """Prueba diferentes configuraciones."""
    print("\n🧪 Prueba 2: Opciones de configuración")
    print("-" * 40)
    
    configs = [
        {
            "name": "Avatar complejo",
            "params": {
                "model_name": "isnet-general-use",
                "min_alpha_threshold": 15,
                "preserve_elements": True,
                "smooth_edges": True
            }
        },
        {
            "name": "Procesamiento rápido", 
            "params": {
                "model_name": "u2net",
                "min_alpha_threshold": 50,
                "preserve_elements": False,
                "smooth_edges": False
            }
        },
        {
            "name": "Calidad premium",
            "params": {
                "model_name": "isnet-general-use",
                "min_alpha_threshold": 10,
                "preserve_elements": True,
                "smooth_edges": True
            }
        }
    ]
    
    for config in configs:
        try:
            bg_remover = TutanchaconBgRemover(**config["params"])
            print(f"✅ {config['name']}: {bg_remover}")
        except Exception as e:
            print(f"❌ Error en {config['name']}: {e}")

def test_parameter_updates():
    """Prueba la actualización de parámetros."""
    print("\n🧪 Prueba 3: Actualización de parámetros")
    print("-" * 40)
    
    try:
        bg_remover = TutanchaconBgRemover()
        
        # Probar cambio de umbral
        print("📊 Probando cambio de umbral...")
        bg_remover.set_threshold(30)
        print(f"✅ Umbral actualizado: {bg_remover.min_alpha_threshold}")
        
        # Probar cambio de modelo
        print("🔄 Probando cambio de modelo...")
        bg_remover.set_model('u2net')
        print(f"✅ Modelo actualizado: {bg_remover.model_name}")
        
        # Probar umbral inválido
        print("🚨 Probando umbral inválido...")
        try:
            bg_remover.set_threshold(300)
            print("❌ No se detectó error con umbral inválido")
        except ValueError:
            print("✅ Error correctamente detectado para umbral inválido")
            
    except Exception as e:
        print(f"❌ Error en prueba de parámetros: {e}")

def test_image_processing():
    """Prueba el procesamiento real de imágenes si están disponibles."""
    print("\n🧪 Prueba 4: Procesamiento de imágenes")
    print("-" * 40)
    
    # Buscar imágenes de prueba
    test_images = [
        "avatar_formato ejemplo/avatar_136x234.png",
        "avatar_formato ejemplo/avatar_204x175.png",
        "avatar_formato ejemplo/avatar_38x38.png"
    ]
    
    available_images = [img for img in test_images if os.path.exists(img)]
    
    if not available_images:
        print("⚠️ No se encontraron imágenes de prueba")
        print("💡 Coloca algunas imágenes en 'avatar_formato ejemplo/' para probar")
        return
    
    try:
        bg_remover = TutanchaconBgRemover(
            min_alpha_threshold=20,
            preserve_elements=True,
            smooth_edges=True
        )
        
        # Crear directorio de salida
        output_dir = "test_output"
        os.makedirs(output_dir, exist_ok=True)
        
        for img_path in available_images[:2]:  # Procesar máximo 2 imágenes para la prueba
            print(f"📸 Procesando: {img_path}")
            
            # Obtener estadísticas si está disponible
            stats = bg_remover.get_stats(img_path)
            if stats:
                print(f"📊 Estadísticas: {stats}")
            
            # Procesar imagen
            output_path = os.path.join(output_dir, f"processed_{os.path.basename(img_path)}")
            bg_remover.remove_background(img_path, output_path)
            
            if os.path.exists(output_path):
                print(f"✅ Imagen procesada: {output_path}")
            else:
                print(f"❌ No se generó la imagen de salida: {output_path}")
                
    except Exception as e:
        print(f"❌ Error en procesamiento de imágenes: {e}")
        print("💡 Asegúrate de que bgremover esté correctamente instalado")

def main():
    """Función principal de pruebas."""
    print("🎨 Pruebas de TutanchaconBgRemover")
    print("=" * 50)
    
    # Ejecutar todas las pruebas
    bg_remover = test_basic_usage()
    
    if bg_remover is not None:
        test_configuration_options()
        test_parameter_updates()
        test_image_processing()
        
        print("\n🎉 Pruebas completadas!")
        print("\n💡 Siguiente paso: Usar en tu aplicación:")
        print("   from src.tutanchacon_bg_remover import TutanchaconBgRemover")
        print("   bg_remover = TutanchaconBgRemover()")
        print("   bg_remover.remove_background('input.jpg', 'output.png')")
    else:
        print("\n❌ Las pruebas básicas fallaron")
        print("🔧 Ejecuta setup_bgremover.bat para configurar bgremover")

if __name__ == "__main__":
    main()
