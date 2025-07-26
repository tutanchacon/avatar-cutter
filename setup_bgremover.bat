@echo off
echo.
echo ===============================================
echo  Configurando bgremover de tutanchacon
echo ===============================================
echo.

REM Activar entorno virtual si existe
if exist "avatarprocess_env\Scripts\activate.bat" (
    echo 🔄 Activando entorno virtual...
    call avatarprocess_env\Scripts\activate.bat
)

echo 📦 Instalando dependencias de bgremover...
pip install -r bgremover_requirements.txt

echo.
echo 📥 Clonando repositorio bgremover...
if not exist "bgremover" (
    git clone https://github.com/tutanchacon/bgremover.git
) else (
    echo ⚠️  El directorio bgremover ya existe, actualizando...
    cd bgremover
    git pull
    cd ..
)

echo.
echo 🔧 Instalando bgremover como paquete...
cd bgremover
pip install -e .
cd ..

echo.
echo ✅ Configuración completada!
echo.
echo 🎯 Ahora puedes usar TutanchaconBgRemover en tu proyecto:
echo    python example_tutanchacon_bg_remover.py
echo.
pause
