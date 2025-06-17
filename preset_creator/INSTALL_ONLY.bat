@echo off
title OrtoIoT Preset Creator - Installazione
color 0B
echo.
echo =====================================
echo  OrtoIoT Preset Creator - Install
echo =====================================
echo.

:: Controlla Python
echo Controllo Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non installato!
    echo.
    echo ISTRUZIONI:
    echo 1. Vai su https://www.python.org/downloads/
    echo 2. Scarica Python (versione 3.8 o superiore)
    echo 3. Durante installazione, spunta "Add Python to PATH"
    echo 4. Riavvia questo script
    echo.
    start https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ %PYTHON_VERSION% trovato!
echo.

:: Aggiorna pip
echo Aggiornamento pip...
python -m pip install --upgrade pip --quiet

:: Installa dipendenze una per una
echo.
echo Installazione dipendenze:
echo.

echo [1/2] Installazione customtkinter...
python -m pip install customtkinter
if %errorlevel% equ 0 (
    echo ✅ customtkinter installato con successo
) else (
    echo ⚠️ customtkinter non installato - useremo tkinter standard
)

echo.
echo [2/2] Installazione pillow...
python -m pip install pillow
if %errorlevel% equ 0 (
    echo ✅ pillow installato con successo
) else (
    echo ⚠️ pillow non installato - alcune funzioni potrebbero non funzionare
)

echo.
echo ========================================
echo  ✅ INSTALLAZIONE COMPLETATA!
echo ========================================
echo.
echo Ora puoi:
echo 1. Avviare il programma con: RUN_PROGRAM.bat
echo 2. Oppure manualmente con: python preset_creator.py
echo.
pause