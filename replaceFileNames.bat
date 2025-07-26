@echo off
setlocal enabledelayedexpansion
set "main_directory=D:\wamp64\www\avatarImageProcessor\p4_croppedimages"

:: Buscar recursivamente carpetas con "_art_of_a" en el nombre
for /d /r "%main_directory%" %%d in (*_art_of_a*) do (
    set "dir=%%d"
    set "folder_name=%%~nd"
    set "parent_dir=%%~pd"
    
    :: Reemplazar "_art_of_a" en el nombre del directorio
    set "new_folder_name=!folder_name:_art_of_a=!"
    
    :: Renombrar el directorio
    ren "%%d" "!new_folder_name!"
)

echo Renombrado completo.
pause
