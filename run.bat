@echo off
REM Script de lancement pour P_Creator (Windows)

echo 🚀 Lancement de P_Creator V6.0...
echo 📁 Répertoire : %CD%

REM Vérification de Python3
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python n'est pas installé
    pause
    exit /b 1
)

REM Vérification de PySide6
python -c "import PySide6" >nul 2>&1
if errorlevel 1 (
    echo 📦 Installation de PySide6...
    pip install PySide6
)

REM Lancement de l'application
echo 🎯 Lancement de l'application...
python main.py
pause


