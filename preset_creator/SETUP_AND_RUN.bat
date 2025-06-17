@echo off
title OrtoIoT Preset Creator - Auto Setup
color 0A
echo.
echo ========================================
echo  OrtoIoT Preset Creator - Auto Setup
echo ========================================
echo.

:: Controlla se Python è installato
echo [1/5] Controllo Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python non trovato!
    echo.
    echo Per favore installa Python da: https://www.python.org/downloads/
    echo Assicurati di spuntare "Add Python to PATH" durante l'installazione
    echo.
    pause
    exit /b 1
)

python --version
echo ✅ Python trovato!
echo.

:: Controlla se pip è disponibile
echo [2/5] Controllo pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip non trovato!
    echo Installazione pip...
    python -m ensurepip --upgrade
)
echo ✅ pip disponibile!
echo.

:: Installa dipendenze
echo [3/5] Installazione dipendenze...
echo Installazione customtkinter...
python -m pip install customtkinter --quiet
if %errorlevel% neq 0 (
    echo ⚠️ Errore installazione customtkinter, provo con tkinter standard
) else (
    echo ✅ customtkinter installato
)

echo Installazione pillow...
python -m pip install pillow --quiet
if %errorlevel% neq 0 (
    echo ⚠️ Errore installazione pillow, continuo senza
) else (
    echo ✅ pillow installato
)
echo.

:: Controlla se il file principale esiste
echo [4/5] Controllo file programma...
if not exist "preset_creator.py" (
    echo ❌ File preset_creator.py non trovato!
    echo.
    echo Assicurati che i seguenti file siano nella stessa cartella di questo batch:
    echo - preset_creator.py
    echo - SETUP_AND_RUN.bat
    echo.
    pause
    exit /b 1
)
echo ✅ File programma trovato!
echo.

:: Avvia il programma
echo [5/5] Avvio OrtoIoT Preset Creator...
echo.
echo 🚀 Avvio in corso...
echo.

python preset_creator.py

:: Se il programma si chiude con errore
if %errorlevel% neq 0 (
    echo.
    echo ❌ Il programma si è chiuso con errore.
    echo.
    echo Debug info:
    echo - Codice errore: %errorlevel%
    echo - Prova ad avviare manualmente: python preset_creator.py
    echo.
    pause
    exit /b %errorlevel%
)

:: Programma chiuso normalmente
echo.
echo ✅ Programma chiuso correttamente.
echo.
echo Grazie per aver usato OrtoIoT Preset Creator!
echo.
pause