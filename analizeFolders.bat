@echo off
setlocal enabledelayedexpansion

:: Ruta del directorio principal (modifica esto según sea necesario)
set "DIR_INICIAL=D:\wamp64\www\avatarImageProcessor\p4_croppedimages\"

:: Archivo de log de errores
set "ERROR_LOG=error_log.txt"

:: Limpiar archivo de log si ya existe
if exist "%ERROR_LOG%" del "%ERROR_LOG%"

:: Recorrer todos los directorios
echo Buscando directorios terminales con conteo diferente a 6...

for /d /r "%DIR_INICIAL%" %%D in (*) do (
    set "isEmpty=1"
    for /d %%S in ("%%D\*") do (
        set "isEmpty=0"
    )
    if !isEmpty! == 1 (
        set "count=0"
        for %%F in ("%%D\*.*") do (
            set /a count+=1
        )
        if not !count! == 6 (
            echo Directorio: "%%D" - Archivos: !count! >> "%ERROR_LOG%"
        )
    )
)

echo Proceso finalizado. Revisa "%ERROR_LOG%" para ver los resultados.
pause
