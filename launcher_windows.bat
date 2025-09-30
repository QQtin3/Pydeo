@echo off

:: Configuration de l'environnement
set "VENV_DIR=venv"
set "PYTHON_EXEC=python.exe"

:: Création de l'environnement virtuel
if not exist "%VENV_DIR%" (
    echo 🔹 Creating virtual environment...
    "%PYTHON_EXEC%" -m venv "%VENV_DIR%"
    
    :: Installation des dépendances
    if exist requirements.txt (
        echo 📦 Installing dependencies from requirements.txt...
        "%VENV_DIR%\Scripts\pip.exe" install -r requirements.txt >nul
    ) else (
        echo ⚠️  No requirements.txt found. Installing PySide6 by default...
        "%VENV_DIR%\Scripts\pip.exe" install PySide6 >nul
    )
)

:: Détermination dynamique des chemins
set "SITE_PACKAGES="
for /f "delims=" %%i in ('""%VENV_DIR%\Scripts\python.exe" -c "import sysconfig; print(sysconfig.get_paths()['purelib'])" 2^>nul"') do set "SITE_PACKAGES=%%i"

if not defined SITE_PACKAGES (
    echo ❌ Error: Failed to determine Python site-packages directory.
    echo    Please ensure Python is properly installed in the virtual environment.
    exit /b 1
)

:: Configuration spécifique Qt pour Windows
set "QT_PLUGINS_DIR=%SITE_PACKAGES%\PySide6\Qt\plugins"
set "QT_BIN_DIR=%SITE_PACKAGES%\PySide6\Qt\bin"

:: Vérification des chemins Qt
if not exist "%QT_PLUGINS_DIR%\" (
    echo ❌ Error: Qt plugins directory not found (%QT_PLUGINS_DIR%)
    echo    Ensure PySide6 is properly installed (^> pip install --force-reinstall PySide6^)
    exit /b 1
)

if not exist "%QT_BIN_DIR%\" (
    echo ❌ Error: Qt binaries directory not found (%QT_BIN_DIR%)
    echo    Ensure PySide6 is properly installed (^> pip install --force-reinstall PySide6^)
    exit /b 1
)

:: Configuration de l'environnement
set "QT_DEBUG_PLUGINS=1"
set "QT_PLUGIN_PATH=%QT_PLUGINS_DIR%"
set "PATH=%QT_BIN_DIR%;%PATH%"

:: Affichage des informations de débogage
echo.
echo ⚙️  Environment Configuration:
echo    QT_PLUGIN_PATH = %QT_PLUGIN_PATH%
echo    PATH (with Qt binaries) = %PATH%
echo    Python version: "%VENV_DIR%\Scripts\python.exe" --version
"%VENV_DIR%\Scripts\python.exe" --version 2>&1

:: Démarrage de l'application
echo.
echo 🚀 Starting application...
call "%VENV_DIR%\Scripts\python.exe" main.py
exit /b %errorlevel%