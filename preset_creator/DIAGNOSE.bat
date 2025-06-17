@echo off
title OrtoIoT Preset Creator - Diagnostica
color 0E
echo.
echo ==========================================
echo  OrtoIoT Preset Creator - DIAGNOSTICA
echo ==========================================
echo.

:: Sistema operativo
echo [SISTEMA]
echo OS: %OS%
echo Architettura: %PROCESSOR_ARCHITECTURE%
echo Computer: %COMPUTERNAME%
echo Usuario: %USERNAME%
echo.

:: Controlla Python
echo [PYTHON]
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version') do echo ✅ Python: %%i
    
    :: Percorso Python
    for /f "tokens=*" %%i in ('where python') do echo    Percorso: %%i
    
    :: Controlla pip
    python -m pip --version >nul 2>&1
    if %errorlevel% equ 0 (
        for /f "tokens=*" %%i in ('python -m pip --version') do echo ✅ pip: %%i
    ) else (
        echo ❌ pip non disponibile
    )
) else (
    echo ❌ Python NON INSTALLATO
    echo.
    echo SOLUZIONE:
    echo 1. Vai su https://www.python.org/downloads/
    echo 2. Scarica Python 3.8 o superiore
    echo 3. Durante installazione SPUNTA "Add Python to PATH"
    echo 4. Riavvia computer
    echo.
)
echo.

:: Controlla file necessari  
echo [FILE NECESSARI]
if exist "preset_creator.py" (
    echo ✅ preset_creator.py trovato
    for %%A in (preset_creator.py) do echo    Dimensione: %%~zA bytes
) else (
    echo ❌ preset_creator.py MANCANTE
)

if exist "requirements.txt" (
    echo ✅ requirements.txt trovato
) else (
    echo ⚠️ requirements.txt mancante (opzionale)
)

if exist "SETUP_AND_RUN.bat" (
    echo ✅ SETUP_AND_RUN.bat trovato
) else (
    echo ⚠️ SETUP_AND_RUN.bat mancante
)
echo.

:: Controlla dipendenze Python
echo [DIPENDENZE PYTHON]
if %errorlevel% equ 0 (
    echo Controllo moduli installati...
    
    python -c "import tkinter; print('✅ tkinter (standard)')" 2>nul
    if %errorlevel% neq 0 echo ❌ tkinter non disponibile
    
    python -c "import customtkinter; print('✅ customtkinter')" 2>nul
    if %errorlevel% neq 0 echo ⚠️ customtkinter non installato (userà tkinter standard)
    
    python -c "import PIL; print('✅ pillow (PIL)')" 2>nul
    if %errorlevel% neq 0 echo ⚠️ pillow non installato (alcune funzioni limitate)
    
    python -c "import json; print('✅ json (standard)')" 2>nul
    python -c "import os; print('✅ os (standard)')" 2>nul
    python -c "import datetime; print('✅ datetime (standard)')" 2>nul
    python -c "import uuid; print('✅ uuid (standard)')" 2>nul
) else (
    echo ❌ Impossibile controllare - Python non disponibile
)
echo.

:: Test di avvio
echo [TEST AVVIO]
if exist "preset_creator.py" (
    echo Tentativo avvio programma per 5 secondi...
    timeout /t 2 /nobreak >nul
    
    python -c "
import sys
try:
    import tkinter as tk
    print('✅ Interfaccia grafica disponibile')
    
    # Test creazione finestra
    root = tk.Tk()
    root.withdraw()
    print('✅ Finestra test OK')
    root.destroy()
    
except ImportError as e:
    print('❌ Errore import:', e)
except Exception as e:
    print('❌ Errore generico:', e)
    " 2>nul
    
    if %errorlevel% equ 0 (
        echo ✅ Test avvio SUPERATO
    ) else (
        echo ❌ Test avvio FALLITO
    )
) else (
    echo ❌ Impossibile testare - file programma mancante
)
echo.

:: Suggerimenti
echo [SUGGERIMENTI]
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔧 INSTALLA PYTHON:
    echo    1. https://www.python.org/downloads/
    echo    2. Spunta "Add Python to PATH"
    echo    3. Riavvia computer
    echo.
)

if not exist "preset_creator.py" (
    echo 🔧 SCARICA FILE PROGRAMMA:
    echo    1. Assicurati di avere preset_creator.py
    echo    2. Metti tutti i file nella stessa cartella
    echo.
)

python -c "import customtkinter" >nul 2>&1
if %errorlevel% neq 0 (
    echo 🔧 INSTALLA DIPENDENZE:
    echo    1. Esegui: pip install customtkinter pillow
    echo    2. Oppure usa: INSTALL_ONLY.bat
    echo.
)

echo ==========================================
echo  Diagnostica completata!
echo ==========================================
echo.
echo Se tutto è ✅ verde, prova: SETUP_AND_RUN.bat
echo Se ci sono ❌ errori, segui i suggerimenti sopra.
echo.
pause