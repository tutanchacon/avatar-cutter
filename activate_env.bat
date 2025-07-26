@echo off
echo Activando entorno virtual de Avatar Image Processor...
echo.

if not exist "avatarprocess_env" (
    echo ERROR: No se encontro el entorno virtual avatarprocess_env
    echo Ejecuta primero: python install.py
    pause
    exit /b 1
)

echo Activando entorno virtual...
call avatarprocess_env\Scripts\activate.bat

echo.
echo ================================================
echo   Avatar Image Processor - Entorno Activado
echo ================================================
echo.
echo Comandos disponibles:
echo   python remove_bg.py      - Remover fondos
echo   python resize_images.py  - Redimensionar imagenes
echo   python check_system.py   - Verificar sistema
echo.
echo Para desactivar: deactivate
echo.

cmd /k
