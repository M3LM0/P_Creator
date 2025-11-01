#!/bin/bash
# Script de build pour créer l'exécutable P_Creator avec PyInstaller

echo "🔨 Construction de l'exécutable P_Creator..."
echo "=============================================="
echo ""

# Vérifier que le venv est activé ou utiliser celui du projet
if [ -d ".venv" ]; then
    PYTHON=".venv/bin/python"
    echo "✅ Utilisation du venv local"
else
    PYTHON="python3"
    echo "⚠️  Utilisation de python3 système"
fi

# Vérifier que PyInstaller est installé
if ! $PYTHON -c "import PyInstaller" 2>/dev/null; then
    echo "📦 Installation de PyInstaller..."
    $PYTHON -m pip install pyinstaller
fi

# Nettoyer les anciens builds
echo "🧹 Nettoyage des anciens builds..."
rm -rf build/ dist/ __pycache__/
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Construire l'exécutable
echo "🔨 Construction de l'exécutable..."
$PYTHON -m PyInstaller p_creator.spec --clean --noconfirm

# Vérifier le résultat
if [ -f "dist/P_Creator" ]; then
    echo ""
    echo "✅ Exécutable créé avec succès !"
    echo "📂 Chemin : $(pwd)/dist/P_Creator"
    echo ""
    echo "📊 Taille de l'exécutable :"
    ls -lh dist/P_Creator | awk '{print "   " $5}'
    echo ""
    echo "🚀 Pour tester l'exécutable :"
    echo "   ./dist/P_Creator"
else
    echo ""
    echo "❌ Erreur : L'exécutable n'a pas été créé"
    exit 1
fi

