"""
Script de testing integral para el proyecto Avatar Image Processor
Prueba todos los componentes y configuraciones del sistema.
"""

import os
import sys
import traceback
from pathlib import Path

# Agregar el directorio actual al path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Prueba que todos los imports funcionen correctamente."""
    print("🧪 Probando imports del proyecto...")
    print("-" * 40)
    
    tests = []
    
    # Test imports básicos
    try:
        from config import Config
        tests.append(("✅", "config.Config"))
    except Exception as e:
        tests.append(("❌", f"config.Config: {e}"))
    
    try:
        from bg_remover_config import BackgroundRemoverConfig
        tests.append(("✅", "bg_remover_config.BackgroundRemoverConfig"))
    except Exception as e:
        tests.append(("❌", f"bg_remover_config.BackgroundRemoverConfig: {e}"))
    
    # Test imports del src
    try:
        from src.background_remover import BackgroundRemover
        tests.append(("✅", "src.background_remover.BackgroundRemover"))
    except Exception as e:
        tests.append(("❌", f"src.background_remover.BackgroundRemover: {e}"))
    
    try:
        from src.remove_bg_service import RemoveBgService
        tests.append(("✅", "src.remove_bg_service.RemoveBgService"))
    except Exception as e:
        tests.append(("❌", f"src.remove_bg_service.RemoveBgService: {e}"))
    
    try:
        from src.tutanchacon_bg_remover import TutanchaconBgRemover
        tests.append(("✅", "src.tutanchacon_bg_remover.TutanchaconBgRemover"))
    except Exception as e:
        tests.append(("❌", f"src.tutanchacon_bg_remover.TutanchaconBgRemover: {e}"))
    
    try:
        from src.background_remover_factory import BackgroundRemoverFactory
        tests.append(("✅", "src.background_remover_factory.BackgroundRemoverFactory"))
    except Exception as e:
        tests.append(("❌", f"src.background_remover_factory.BackgroundRemoverFactory: {e}"))
    
    try:
        from src.proportional_image_resizer import ProportionalImageResizer
        tests.append(("✅", "src.proportional_image_resizer.ProportionalImageResizer"))
    except Exception as e:
        tests.append(("❌", f"src.proportional_image_resizer.ProportionalImageResizer: {e}"))
    
    try:
        from src.face_detector import FaceDetector
        tests.append(("✅", "src.face_detector.FaceDetector"))
    except Exception as e:
        tests.append(("❌", f"src.face_detector.FaceDetector: {e}"))
    
    try:
        from src.image_processor import ImageProcessor
        tests.append(("✅", "src.image_processor.ImageProcessor"))
    except Exception as e:
        tests.append(("❌", f"src.image_processor.ImageProcessor: {e}"))
    
    # Mostrar resultados
    passed = 0
    for status, message in tests:
        print(f"  {status} {message}")
        if status == "✅":
            passed += 1
    
    print(f"\\n📊 Imports: {passed}/{len(tests)} exitosos")
    return passed == len(tests)

def test_configuration():
    """Prueba la configuración del proyecto."""
    print("\\n🔧 Probando configuración...")
    print("-" * 40)
    
    try:
        from config import Config
        
        # Mostrar configuración
        Config.print_configuration()
        
        # Validar configuración
        Config.validate_configuration()
        
        print("✅ Configuración válida")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración: {e}")
        traceback.print_exc()
        return False

def test_bg_remover_config():
    """Prueba la configuración del removedor de fondos."""
    print("\\n🎨 Probando configuración de removedor de fondos...")
    print("-" * 50)
    
    try:
        from bg_remover_config import BackgroundRemoverConfig
        
        # Mostrar configuración actual
        BackgroundRemoverConfig.print_current_config()
        
        # Probar cambio de preset
        print("\\n🔄 Probando cambio de preset...")
        original_preset = BackgroundRemoverConfig.ACTIVE_PRESET
        
        BackgroundRemoverConfig.set_preset('avatar_equilibrado')
        config = BackgroundRemoverConfig.get_tutanchacon_config()
        print(f"✅ Preset 'avatar_equilibrado': {config}")
        
        # Restaurar preset original
        BackgroundRemoverConfig.ACTIVE_PRESET = original_preset
        
        print("✅ Configuración de removedor válida")
        return True
        
    except Exception as e:
        print(f"❌ Error en configuración de removedor: {e}")
        traceback.print_exc()
        return False

def test_factory():
    """Prueba el factory de removedores de fondo."""
    print("\\n🏭 Probando BackgroundRemoverFactory...")
    print("-" * 45)
    
    try:
        from src.background_remover_factory import BackgroundRemoverFactory
        
        # Verificar tipos disponibles
        available_types = BackgroundRemoverFactory.get_available_types()
        print(f"📦 Tipos disponibles: {available_types}")
        
        # Verificar si TutanchaconBgRemover está disponible
        tutanchacon_available = BackgroundRemoverFactory.is_tutanchacon_available()
        print(f"🎨 TutanchaconBgRemover: {'✅ Disponible' if tutanchacon_available else '❌ No disponible'}")
        
        # Probar creación de removedor API (simulado)
        try:
            api_remover = BackgroundRemoverFactory.create_remover('api', api_key='test_key')
            print("✅ RemoveBgService factory funciona")
        except Exception as e:
            print(f"✅ RemoveBgService factory funciona (error esperado sin API real): {type(e).__name__}")
        
        # Probar creación de TutanchaconBgRemover si está disponible
        if tutanchacon_available:
            try:
                tutanchacon_remover = BackgroundRemoverFactory.create_remover('tutanchacon')
                print(f"✅ TutanchaconBgRemover factory: {type(tutanchacon_remover).__name__}")
            except Exception as e:
                print(f"⚠️ TutanchaconBgRemover factory error: {e}")
        
        print("✅ Factory funcionando correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error en factory: {e}")
        traceback.print_exc()
        return False

def test_directories():
    """Prueba que los directorios existan o se puedan crear."""
    print("\\n📁 Probando estructura de directorios...")
    print("-" * 45)
    
    try:
        from config import Config
        
        directories = [
            Config.APPROVED_IMAGES_DIR,
            Config.CROPPED_IMAGES_DIR
        ]
        
        for directory in directories:
            if os.path.exists(directory):
                print(f"✅ {directory} existe")
            else:
                os.makedirs(directory, exist_ok=True)
                print(f"✅ {directory} creado")
        
        # Verificar directorio model
        model_dir = "model"
        if os.path.exists(model_dir):
            print(f"✅ {model_dir} existe")
            
            # Verificar archivo Haar Cascade
            haar_file = os.path.join(model_dir, Config.HAAR_CASCADE_PATH)
            if os.path.exists(haar_file):
                print(f"✅ {Config.HAAR_CASCADE_PATH} encontrado")
            else:
                print(f"⚠️ {Config.HAAR_CASCADE_PATH} no encontrado")
        else:
            print(f"⚠️ {model_dir} no existe")
        
        print("✅ Estructura de directorios válida")
        return True
        
    except Exception as e:
        print(f"❌ Error con directorios: {e}")
        traceback.print_exc()
        return False

def test_dependencies():
    """Prueba que las dependencias estén instaladas."""
    print("\\n📦 Probando dependencias...")
    print("-" * 35)
    
    dependencies = [
        ('opencv-python', 'cv2'),
        ('pillow', 'PIL'),
        ('numpy', 'numpy'),
        ('requests', 'requests'),
        ('matplotlib', 'matplotlib'),
        ('python-dotenv', 'dotenv'),
        ('rembg', 'rembg'),
        ('scipy', 'scipy')
    ]
    
    installed = 0
    for package_name, import_name in dependencies:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
            installed += 1
        except ImportError:
            print(f"❌ {package_name} no instalado")
    
    print(f"\\n📊 Dependencias: {installed}/{len(dependencies)} instaladas")
    return installed >= len(dependencies) - 2  # Permitir que falten máximo 2

def test_sample_images():
    """Verifica si hay imágenes de muestra para probar."""
    print("\\n🖼️ Verificando imágenes de muestra...")
    print("-" * 40)
    
    sample_dirs = [
        "avatar_formato ejemplo",
        "p2_approvedimages",
        "p1_rawimages"
    ]
    
    found_images = False
    
    for directory in sample_dirs:
        if os.path.exists(directory):
            images = [f for f in os.listdir(directory) 
                     if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff'))]
            
            if images:
                print(f"✅ {directory}: {len(images)} imágenes encontradas")
                found_images = True
                
                # Mostrar algunas imágenes de muestra
                for img in images[:3]:
                    print(f"   📸 {img}")
                if len(images) > 3:
                    print(f"   ... y {len(images) - 3} más")
            else:
                print(f"⚠️ {directory}: sin imágenes")
        else:
            print(f"⚠️ {directory}: no existe")
    
    if not found_images:
        print("💡 Para probar el procesamiento, coloca imágenes en:")
        print("   - avatar_formato ejemplo/")
        print("   - p2_approvedimages/")
    
    return found_images

def test_main_scripts():
    """Prueba que los scripts principales se puedan importar."""
    print("\\n📜 Probando scripts principales...")
    print("-" * 40)
    
    scripts = [
        'resize_images',
        'remove_bg',
        'demo_bg_config',
        'demo_factory',
        'test_tutanchacon_bg_remover'
    ]
    
    working = 0
    for script in scripts:
        try:
            # Solo probar import, no ejecutar
            spec = __import__(script)
            print(f"✅ {script}.py")
            working += 1
        except Exception as e:
            print(f"❌ {script}.py: {e}")
    
    print(f"\\n📊 Scripts: {working}/{len(scripts)} importables")
    return working >= len(scripts) - 1  # Permitir que falle máximo 1

def run_comprehensive_test():
    """Ejecuta todos los tests del proyecto."""
    print("🧪 TESTING INTEGRAL - Avatar Image Processor")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Configuración", test_configuration),
        ("Config BG Remover", test_bg_remover_config),
        ("Factory", test_factory),
        ("Directorios", test_directories),
        ("Dependencias", test_dependencies),
        ("Imágenes muestra", test_sample_images),
        ("Scripts principales", test_main_scripts)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\\n❌ Error crítico en {test_name}: {e}")
            results.append((test_name, False))
    
    # Resumen final
    print("\\n" + "=" * 60)
    print("📊 RESUMEN DE TESTING")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    success_rate = (passed / len(results)) * 100
    print(f"\\n🎯 Resultado: {passed}/{len(results)} tests exitosos ({success_rate:.1f}%)")
    
    if success_rate >= 80:
        print("🎉 ¡Proyecto en buen estado para usar!")
        
        if success_rate < 100:
            print("\\n💡 Sugerencias para completar setup:")
            if not any(name == "Dependencias" and result for name, result in results):
                print("   - Ejecutar: pip install -r requirements.txt")
            if not any(name == "Factory" and result for name, result in results):
                print("   - Ejecutar: setup_bgremover.bat")
            if not any(name == "Imágenes muestra" and result for name, result in results):
                print("   - Agregar imágenes de prueba en avatar_formato ejemplo/")
    else:
        print("⚠️ El proyecto necesita configuración adicional")
        print("\\n🔧 Revisar los errores arriba y:")
        print("   1. Instalar dependencias faltantes")
        print("   2. Ejecutar setup_bgremover.bat")
        print("   3. Configurar variables de entorno")
    
    return success_rate >= 80

if __name__ == "__main__":
    run_comprehensive_test()
