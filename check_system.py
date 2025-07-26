#!/usr/bin/env python3
"""
Script de verificación del sistema para Avatar Image Processor
Diagnostica la configuración y dependencias del proyecto
"""

import os
import sys
import subprocess
import importlib
from pathlib import Path

def check_python_version():
    """Verifica la versión de Python"""
    version = sys.version_info
    print(f"🐍 Python: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        return False
    else:
        print("✅ Versión de Python compatible")
        return True

def check_virtual_environment():
    """Verifica si está en un entorno virtual"""
    venv_path = Path("avatarprocess_env")
    in_venv = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    
    print(f"🏠 Entorno virtual:")
    if venv_path.exists():
        print(f"✅ Directorio del entorno virtual existe: {venv_path}")
    else:
        print(f"❌ No se encontró el directorio del entorno virtual: {venv_path}")
        return False
    
    if in_venv:
        print(f"✅ Ejecutándose en entorno virtual: {sys.prefix}")
    else:
        print("⚠️  No se está ejecutando en un entorno virtual")
        print("   Para activar: avatarprocess_env\\Scripts\\activate (Windows)")
        print("   Para activar: source avatarprocess_env/bin/activate (Unix/Linux)")
    
    return True

def check_dependencies():
    """Verifica las dependencias principales"""
    dependencies = {
        'cv2': 'opencv-python',
        'PIL': 'pillow', 
        'numpy': 'numpy',
        'requests': 'requests',
        'matplotlib': 'matplotlib',
        'dotenv': 'python-dotenv'
    }
    
    print("📦 Verificando dependencias:")
    all_ok = True
    
    for module, package in dependencies.items():
        try:
            importlib.import_module(module)
            print(f"✅ {package} instalado")
        except ImportError:
            print(f"❌ {package} NO instalado")
            all_ok = False
    
    return all_ok

def check_opencv_data():
    """Verifica que los datos de OpenCV estén disponibles"""
    try:
        import cv2
        haar_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
        if os.path.exists(haar_path):
            print(f"✅ Haar Cascade encontrado: {haar_path}")
            return True
        else:
            print(f"❌ Haar Cascade NO encontrado: {haar_path}")
            return False
    except Exception as e:
        print(f"❌ Error verificando OpenCV: {e}")
        return False

def check_configuration():
    """Verifica la configuración del proyecto"""
    print("⚙️  Verificando configuración:")
    
    # Verificar archivo .env
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ Archivo .env encontrado")
        
        # Verificar API key
        try:
            from config import Config
            if Config.validate_api_key():
                print("✅ API key de remove.bg configurada")
            else:
                print("❌ API key de remove.bg NO configurada")
                print("   Configura REMOVE_BG_API_KEY en el archivo .env")
                return False
        except Exception as e:
            print(f"❌ Error al verificar configuración: {e}")
            return False
    else:
        print("❌ Archivo .env NO encontrado")
        if env_example.exists():
            print("💡 Copia .env.example a .env y configura tus valores")
        return False
    
    return True

def check_directories():
    """Verifica que existan los directorios necesarios"""
    directories = [
        "src",
        "model", 
        "p1_rawimages",
        "p2_approvedimages",
        "p3_bgremoved", 
        "p4_croppedimages"
    ]
    
    print("📁 Verificando directorios:")
    all_ok = True
    
    for directory in directories:
        path = Path(directory)
        if path.exists():
            print(f"✅ {directory}/")
        else:
            print(f"❌ {directory}/ NO existe")
            if directory.startswith('p'):
                print(f"   Puedes crearlo con: mkdir {directory}")
            all_ok = False
    
    return all_ok

def check_model_files():
    """Verifica que existan los archivos del modelo"""
    model_files = [
        "model/deploy.prototxt",
        "model/res10_300x300_ssd_iter_140000_fp16.caffemodel"
    ]
    
    print("🤖 Verificando archivos del modelo:")
    all_ok = True
    
    for file_path in model_files:
        path = Path(file_path)
        if path.exists():
            size = path.stat().st_size
            print(f"✅ {file_path} ({size} bytes)")
        else:
            print(f"❌ {file_path} NO encontrado")
            all_ok = False
    
    return all_ok

def check_main_scripts():
    """Verifica que existan los scripts principales"""
    scripts = [
        "remove_bg.py",
        "resize_images.py",
        "config.py"
    ]
    
    print("📄 Verificando scripts principales:")
    all_ok = True
    
    for script in scripts:
        path = Path(script)
        if path.exists():
            print(f"✅ {script}")
        else:
            print(f"❌ {script} NO encontrado")
            all_ok = False
    
    return all_ok

def run_diagnostic():
    """Ejecuta un diagnóstico completo del sistema"""
    print("🔍 Avatar Image Processor - Diagnóstico del Sistema")
    print("=" * 60)
    
    checks = [
        ("Versión de Python", check_python_version),
        ("Entorno Virtual", check_virtual_environment), 
        ("Dependencias", check_dependencies),
        ("Datos de OpenCV", check_opencv_data),
        ("Configuración", check_configuration),
        ("Directorios", check_directories),
        ("Archivos del Modelo", check_model_files),
        ("Scripts Principales", check_main_scripts)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n--- {name} ---")
        result = check_func()
        results.append((name, result))
    
    # Resumen final
    print("\n" + "=" * 60)
    print("📊 RESUMEN DEL DIAGNÓSTICO")
    print("=" * 60)
    
    passed = 0
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status:<8} {name}")
        if result:
            passed += 1
    
    print(f"\nResultado: {passed}/{len(results)} verificaciones pasaron")
    
    if passed == len(results):
        print("🎉 ¡Todo está configurado correctamente!")
        print("   Puedes ejecutar el proyecto sin problemas.")
    else:
        print("⚠️  Algunos componentes necesitan atención.")
        print("   Revisa los errores arriba y corrige antes de continuar.")
    
    return passed == len(results)

if __name__ == "__main__":
    success = run_diagnostic()
    sys.exit(0 if success else 1)
