@echo off
setlocal enabledelayedexpansion

:: ===============================================
:: Pydeo - Windows Launcher
:: ===============================================

:: Détection automatique du dossier virtuel
if exist "myenv" (
    set "VENV_DIR=myenv"
) else if exist "venv" (
    set "VENV_DIR=venv"
) else (
    echo ❌ No virtual environment found. Creating one in "venv"...
    python -m venv venv
    set "VENV_DIR=venv"
)

set "PYTHON_EXEC=%VENV_DIR%\Scripts\python.exe"
set "PIP_EXEC=%VENV_DIR%\Scripts\pip.exe"

:: Vérifier que Python existe
if not exist "%PYTHON_EXEC%" (
    echo ❌ Error: Could not find Python in %VENV_DIR%.
    exit /b 1
)

:: Installer les dépendances
if exist requirements.txt (
    echo 📦 Installing dependencies from requirements.txt...
    "%PIP_EXEC%" install -r requirements.txt
) else (
    echo ⚠️  No requirements.txt found. Installing PySide6 by default...
    "%PIP_EXEC%" install PySide6
)

:: Détermination du chemin site-packages
set "SITE_PACKAGES="
for /f "usebackq delims=" %%i in (`"%PYTHON_EXEC%" -c "import sysconfig; print(sysconfig.get_paths()['purelib'])" 2^>nul`) do set "SITE_PACKAGES=%%i"

if not defined SITE_PACKAGES (
    echo ❌ Error: Failed to determine Python site-packages directory.
    exit /b 1
)

:: Configuration Qt (plugins + binaires)
set "QT_PLUGINS_DIR=%SITE_PACKAGES%\PySide6\Qt\plugins"
set "QT_BIN_DIR=%SITE_PACKAGES%\PySide6\Qt\bin"

if not exist "%QT_PLUGINS_DIR%\" (
    echo ❌ Error: Qt plugins directory not found (%QT_PLUGINS_DIR%)
    echo    Run: "%PIP_EXEC%" install --force-reinstall PySide6
    exit /b 1
)

if not exist "%QT_BIN_DIR%\" (
    echo ❌ Error: Qt binaries directory not found (%QT_BIN_DIR%)
    echo    Run: "%PIP_EXEC%" install --force-reinstall PySide6
    exit /b 1
)

:: Mise à jour des variables d'environnement
set "QT_DEBUG_PLUGINS=1"
set "QT_PLUGIN_PATH=%QT_PLUGINS_DIR%"
set "PATH=%QT_BIN_DIR%;%PATH%"

:: ===============================================
:: Infos de debug
:: ===============================================
echo.
echo ⚙️  Environment Configuration:
echo    VENV_DIR        = %VENV_DIR%
echo    QT_PLUGIN_PATH  = %QT_PLUGIN_PATH%
echo    Python version:
"%PYTHON_EXEC%" --version 2>&1

:: ===============================================
:: Démarrage de l'application
:: ===============================================
echo.
echo 🚀 Starting application...
call "%PYTHON_EXEC%" main.py
exit /b %errorlevel%
