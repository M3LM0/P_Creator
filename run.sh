#!/bin/bash
# Script de lancement pour P_Creator

echo "🚀 Lancement de P_Creator V6.0..."
echo "📁 Répertoire : $(pwd)"

# Vérification de Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Création de l'environnement virtuel s'il n'existe pas
if [ ! -d ".venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Activation de l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Vérification de PySide6
if ! python -c "import PySide6" 2>/dev/null; then
    echo "📦 Installation de PySide6..."
    pip install PySide6
fi

# Lancement de l'application
echo "🎯 Lancement de l'application..."
python main.py
