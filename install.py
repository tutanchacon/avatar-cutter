#!/usr/bin/env python3
"""
Script de instalación para Avatar Image Processor
Facilita la configuración inicial del proyecto en nuevos equipos
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando del sistema y maneja errores"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}:")
        print(f"   Comando: {command}")
        print(f"   Error: {e.stderr}")
        return False

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} es compatible")
    return True

def create_virtual_environment():
    """Crea el entorno virtual"""
    venv_path = "avatarprocess_env"
    if os.path.exists(venv_path):
        print(f"⚠️  El entorno virtual {venv_path} ya existe")
        response = input("¿Deseas recrearlo? (s/n): ").lower()
        if response == 's':
            print(f"🗑️  Eliminando entorno virtual existente...")
            shutil.rmtree(venv_path)
        else:
            print("📁 Usando entorno virtual existente")
            return True
    
    return run_command(f"python -m venv {venv_path}", "Creando entorno virtual")

def get_pip_command():
    """Obtiene el comando pip apropiado para el sistema"""
    if os.name == 'nt':  # Windows
        return "avatarprocess_env\\Scripts\\pip.exe"
    else:  # Unix/Linux/MacOS
        return "avatarprocess_env/bin/pip"

def install_dependencies():
    """Instala las dependencias del proyecto"""
    pip_cmd = get_pip_command()
    
    commands = [
        (f"{pip_cmd} install --upgrade pip", "Actualizando pip"),
        (f"{pip_cmd} install -r requirements.txt", "Instalando dependencias"),
    ]
    
    for command, description in commands:
        if not run_command(command, description):
            return False
    return True

def setup_configuration():
    """Configura los archivos de configuración"""
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        print("📋 Copiando archivo de configuración de ejemplo...")
        shutil.copy(env_example, env_file)
        print("✅ Archivo .env creado")
        print("⚠️  IMPORTANTE: Edita el archivo .env y configura tu API key de remove.bg")
        return True
    elif env_file.exists():
        print("✅ Archivo .env ya existe")
        return True
    else:
        print("❌ No se encontró archivo .env.example")
        return False

def create_directories():
    """Crea los directorios necesarios del proyecto"""
    directories = [
        "p1_rawimages",
        "p2_approvedimages", 
        "p3_bgremoved",
        "p4_croppedimages"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Directorio {directory} listo")
    
    return True

def main():
    """Función principal de instalación"""
    print("🚀 Instalador de Avatar Image Processor")
    print("=" * 50)
    
    # Verificar versión de Python
    if not check_python_version():
        sys.exit(1)
    
    # Crear entorno virtual
    if not create_virtual_environment():
        print("❌ Error al crear el entorno virtual")
        sys.exit(1)
    
    # Instalar dependencias
    if not install_dependencies():
        print("❌ Error al instalar dependencias")
        sys.exit(1)
    
    # Configurar archivos
    if not setup_configuration():
        print("❌ Error en la configuración")
        sys.exit(1)
    
    # Crear directorios
    if not create_directories():
        print("❌ Error al crear directorios")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 ¡Instalación completada exitosamente!")
    print("\n📝 Próximos pasos:")
    print("1. Edita el archivo .env y configura tu API key de remove.bg")
    print("2. Activa el entorno virtual:")
    
    if os.name == 'nt':  # Windows
        print("   avatarprocess_env\\Scripts\\activate")
    else:  # Unix/Linux/MacOS
        print("   source avatarprocess_env/bin/activate")
    
    print("3. Coloca tus imágenes en p1_rawimages/ o p2_approvedimages/")
    print("4. Ejecuta: python remove_bg.py")
    print("5. Ejecuta: python resize_images.py")
    print("\n🔗 Para más información, consulta el README.md")

if __name__ == "__main__":
    main()
