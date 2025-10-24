#!/bin/bash
# Script de lancement simple pour P_Creator

echo "🚀 P_Creator - Version Simplifiée"
echo "================================="

# Vérifier Python3
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 n'est pas installé"
    exit 1
fi

# Créer l'environnement virtuel s'il n'existe pas
if [ ! -d ".venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python3 -m venv .venv
fi

# Activer l'environnement virtuel
echo "🔧 Activation de l'environnement virtuel..."
source .venv/bin/activate

# Installer PySide6 s'il n'est pas installé
if ! python -c "import PySide6" 2>/dev/null; then
    echo "📥 Installation de PySide6..."
    pip install PySide6
fi

# Lancer l'application
echo "🎯 Lancement de P_Creator..."
python main.py

