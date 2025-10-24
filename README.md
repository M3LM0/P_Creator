# P_Creator - Version Simplifiée

**Créateur de projets avec environnement virtuel automatique**

## 🎯 Objectif

P_Creator simplifie la création de projets en générant automatiquement :
- ✅ **Environnement virtuel** (Python)
- ✅ **Structure de base** du projet
- ✅ **Fichiers de configuration** (requirements.txt, package.json, composer.json)
- ✅ **Scripts d'activation** automatiques
- ✅ **README** avec instructions

## 🚀 Installation et Lancement

### Méthode 1 : Script Automatique (Recommandé)
```bash
./run_simple.sh
```

### Méthode 2 : Manuel
```bash
# Créer l'environnement virtuel
python3 -m venv .venv

# Activer l'environnement virtuel
source .venv/bin/activate

# Installer PySide6
pip install PySide6

# Lancer l'application
python main.py
```

## 🎮 Utilisation

1. **Saisissez le nom** de votre projet
2. **Choisissez le chemin** de destination
3. **Sélectionnez le langage** (Python, JavaScript, PHP)
4. **Choisissez la version** du langage
5. **Cliquez sur "Créer le Projet"**

## 📁 Langages Supportés

### 🐍 Python
- **Versions** : 3.12, 3.11, 3.10, 3.9
- **Environnement virtuel** : Créé automatiquement
- **Fichiers** : main.py, requirements.txt, .gitignore, README.md
- **Script d'activation** : activate.sh / activate.bat

### 🟨 JavaScript (Node.js)
- **Versions** : 20, 18, 16
- **Configuration** : package.json avec scripts
- **Fichiers** : index.js, package.json, .gitignore, README.md

### 🐘 PHP
- **Versions** : 8.3, 8.2, 8.1
- **Configuration** : composer.json
- **Fichiers** : index.php, composer.json, .gitignore, README.md

## 🎯 Exemple de Projet Python Créé

```
mon-projet/
├── .venv/                    # Environnement virtuel
├── main.py                   # Point d'entrée
├── requirements.txt          # Dépendances
├── .gitignore               # Fichiers à ignorer
├── README.md                # Instructions
└── activate.sh              # Script d'activation
```

## 🔧 Commandes Après Création

### Python
```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Installer les dépendances
pip install -r requirements.txt

# Lancer le projet
python main.py
```

### JavaScript
```bash
# Installer les dépendances
npm install

# Lancer le projet
npm start
```

### PHP
```bash
# Installer les dépendances
composer install

# Lancer le projet
php index.php
```

## ✨ Fonctionnalités

- 🎯 **Interface simple** et intuitive
- 🚀 **Création automatique** d'environnements virtuels
- 📁 **Structure de base** générée automatiquement
- 🔧 **Scripts d'activation** pour chaque OS
- 📚 **README complet** avec instructions
- 🎨 **Interface moderne** avec PySide6

## 🛠 Développement

### Structure du Projet
```
P_Creator/
├── main.py                  # Point d'entrée
├── services/
│   ├── language_manager.py  # Gestion des langages
│   └── simple_generator.py  # Générateur de projets
├── run_simple.sh            # Script de lancement
└── README.md               # Documentation
```

### Ajout d'un Nouveau Langage

1. **Modifier** `services/simple_generator.py`
2. **Ajouter** la méthode `_create_xxx_project()`
3. **Ajouter** la méthode `_create_xxx_files()`
4. **Mettre à jour** `supported_languages`

## 🎉 Avantages

- ✅ **Simple** : Interface claire et directe
- ✅ **Rapide** : Création en quelques clics
- ✅ **Automatique** : Environnement virtuel géré automatiquement
- ✅ **Prêt à l'emploi** : Projet immédiatement utilisable
- ✅ **Multi-langages** : Python, JavaScript, PHP
- ✅ **Multi-versions** : Support de plusieurs versions par langage

## 🚀 Prochaines Étapes

Après création de votre projet :
1. **Ouvrez le projet** dans Cursor
2. **Activez l'environnement** (si Python)
3. **Commencez à coder** !

---

**P_Creator** - Simplifiez la création de vos projets ! 🎯