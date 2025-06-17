@echo off
title OrtoIoT Preset Creator
color 0A
cls

echo.
echo  ██████╗ ██████╗ ████████╗ ██████╗ ██╗ ██████╗ ████████╗
echo ██╔═══██╗██╔══██╗╚══██╔══╝██╔═══██╗██║██╔═══██╗╚══██╔══╝
echo ██║   ██║██████╔╝   ██║   ██║   ██║██║██║   ██║   ██║   
echo ██║   ██║██╔══██╗   ██║   ██║   ██║██║██║   ██║   ██║   
echo ╚██████╔╝██║  ██║   ██║   ╚██████╔╝██║╚██████╔╝   ██║   
echo  ╚═════╝ ╚═╝  ╚═╝   ╚═╝    ╚═════╝ ╚═╝ ╚═════╝    ╚═╝   
echo.
echo           Preset Creator v1.0
echo.

:: Controlla se Python è disponibile
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non trovato!
    echo.
    echo Esegui prima: INSTALL_ONLY.bat
    echo.
    pause
    exit /b 1
)

:: Controlla se il file principale esiste
if not exist "preset_creator.py" (
    echo ❌ File preset_creator.py non trovato!
    echo.
    echo Assicurati che preset_creator.py sia nella stessa cartella.
    echo.
    pause
    exit /b 1
)

:: Avvia il programma
echo 🚀 Avvio OrtoIoT Preset Creator...
echo =====================================
echo.

python preset_creator.py

:: Gestisci uscita
echo.
if %errorlevel% equ 0 (
    echo ✅ Programma chiuso correttamente.
) else (
    echo ❌ Errore durante l'esecuzione.
    echo Codice errore: %errorlevel%
    echo.
    echo Prova a eseguire: SETUP_AND_RUN.bat
)
echo.
pause