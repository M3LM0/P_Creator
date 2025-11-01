"""
Générateur simple pour P_Creator
Crée des projets basiques avec environnement virtuel automatique
"""

import os
import subprocess
import shutil
import re
from typing import Dict, List, Optional

class SimpleGenerator:
    """Générateur simple de projets"""
    
    def __init__(self, log_callback=None):
        self.supported_languages = ["Python", "JavaScript", "PHP"]
        self.log_callback = log_callback or print
    
    @staticmethod
    def _normalize_python_version(version_str: str) -> str:
        """
        Normalise une version Python en major.minor
        Exemples: "3.13.0" -> "3.13", "3.9" -> "3.9", "3.10.5" -> "3.10"
        """
        match = re.search(r'^(\d+)\.(\d+)', version_str)
        if match:
            return f"{match.group(1)}.{match.group(2)}"
        return version_str
    
    @staticmethod
    def _extract_python_version_from_output(output: str) -> Optional[str]:
        """
        Extrait la version Python depuis la sortie de 'python --version'
        Exemples: "Python 3.13.0" -> "3.13", "Python 3.9.5" -> "3.9"
        """
        match = re.search(r'(\d+\.\d+)', output)
        if match:
            return match.group(1)
        return None
    
    def create_project(self, name: str, path: str, language: str, version: str, copy_cursor_rules: bool = False) -> str:
        """
        Crée un projet simple avec environnement virtuel
        
        Args:
            name: Nom du projet
            path: Chemin de base
            language: Langage de programmation
            version: Version du langage
            copy_cursor_rules: Copier les règles Cursor (uniquement pour Python)
            
        Returns:
            Chemin complet du projet créé
        """
        # Créer le dossier de base s'il n'existe pas
        os.makedirs(path, exist_ok=True)
        
        # Chemin complet du projet
        project_path = os.path.join(path, name)
        
        # Création du dossier
        os.makedirs(project_path, exist_ok=True)
        
        if language == "Python":
            return self._create_python_project(project_path, version, copy_cursor_rules)
        elif language == "JavaScript":
            return self._create_js_project(project_path, version)
        elif language == "PHP":
            return self._create_php_project(project_path, version)
        else:
            raise ValueError(f"Langage non supporté : {language}")
    
    def _create_python_project(self, project_path: str, version: str, copy_cursor_rules: bool = False) -> str:
        """Crée un projet Python avec environnement virtuel"""
        self.log_callback(f"🐍 Création du projet Python {version}...")
        
        # Création de la structure Python standard
        self._create_python_structure(project_path)
        
        # Copie des règles Cursor si demandée
        if copy_cursor_rules:
            self._copy_cursor_rules(project_path)
        
        # Création de l'environnement virtuel
        venv_path = os.path.join(project_path, ".venv")
        
        # Normaliser la version pour construire les commandes
        normalized_version = self._normalize_python_version(version)
        
        # Essayer plusieurs commandes Python dans l'ordre de préférence
        python_commands = [
            f"python{version}",           # python3.9.24
            f"python{normalized_version}", # python3.9
            "python3",                    # python3 (version par défaut)
            "python"                      # python (version par défaut)
        ]
        
        python_cmd = None
        detected_version = None
        for cmd in python_commands:
            try:
                # Tester si la commande existe et lire stdout + stderr
                result = subprocess.run([cmd, "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    # Combiner stdout et stderr pour la détection
                    output = (result.stdout or '') + (result.stderr or '')
                    detected_version = self._extract_python_version_from_output(output)
                    python_cmd = cmd
                    self.log_callback(f"✅ Python trouvé : {cmd} (version détectée: {detected_version})")
                    break
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                continue
        
        if not python_cmd:
            # Dernier recours : utiliser python3
            python_cmd = "python3"
            try:
                result = subprocess.run([python_cmd, "--version"], capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    output = (result.stdout or '') + (result.stderr or '')
                    detected_version = self._extract_python_version_from_output(output)
            except:
                pass
            self.log_callback(f"⚠️  Utilisation de python3 par défaut")
        
        # Créer le fichier .python-version avec la version réellement détectée
        if detected_version:
            version_for_file = detected_version
        else:
            # Fallback sur la version normalisée de l'entrée utilisateur
            version_for_file = normalized_version
        
        with open(os.path.join(project_path, ".python-version"), "w") as f:
            f.write(version_for_file)
        self.log_callback(f"📝 Fichier .python-version créé avec la version {version_for_file}")
        
        try:
            subprocess.run([python_cmd, "-m", "venv", venv_path], check=True)
            self.log_callback(f"✅ Environnement virtuel créé avec {python_cmd} : {venv_path}")
        except subprocess.CalledProcessError as e:
            self.log_callback(f"❌ Erreur lors de la création de l'environnement virtuel : {e}")
            raise
        
        # Détermination du python selon l'OS
        if os.name == 'nt':  # Windows
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
        else:  # Unix/Linux/macOS
            python_path = os.path.join(venv_path, "bin", "python")
        
        # Création des fichiers de base
        self._create_python_files(project_path, python_path)
        
        # Création du script d'activation
        self._create_activation_script(project_path, venv_path)
        
        # Création du script de vérification
        self._create_check_script(project_path, venv_path)
        
        # Activation automatique et installation des dépendances
        self._activate_and_install_dependencies(project_path, venv_path, python_path)
        
        return project_path
    
    def _create_js_project(self, project_path: str, version: str) -> str:
        """Crée un projet JavaScript avec package.json"""
        self.log_callback(f"🟨 Création du projet JavaScript Node.js {version}...")
        
        # Extraire le numéro de version majeur pour engines.node
        # Exemples: "Node 18" -> "18", "18" -> "18", "Node 20.10.0" -> "20"
        node_major = None
        match = re.search(r'\d+', version)
        if match:
            node_major = match.group(0)
        else:
            node_major = "18"  # Fallback par défaut
        
        # Création du package.json
        package_json = {
            "name": os.path.basename(project_path),
            "version": "1.0.0",
            "description": "Projet JavaScript créé avec P_Creator",
            "main": "index.js",
            "scripts": {
                "start": "node index.js",
                "dev": "node index.js"
            },
            "engines": {
                "node": f">={node_major}.0.0"
            }
        }
        
        import json
        with open(os.path.join(project_path, "package.json"), "w") as f:
            json.dump(package_json, f, indent=2)
        
        # Création des fichiers de base
        self._create_js_files(project_path)
        
        return project_path
    
    def _create_php_project(self, project_path: str, version: str) -> str:
        """Crée un projet PHP avec composer.json"""
        self.log_callback(f"🐘 Création du projet PHP {version}...")
        
        # Création du composer.json
        composer_json = {
            "name": f"vendor/{os.path.basename(project_path)}",
            "description": "Projet PHP créé avec P_Creator",
            "type": "project",
            "require": {
                "php": f">={version}"
            },
            "autoload": {
                "psr-4": {
                    "App\\": "src/"
                }
            }
        }
        
        import json
        with open(os.path.join(project_path, "composer.json"), "w") as f:
            json.dump(composer_json, f, indent=2)
        
        # Création des fichiers de base
        self._create_php_files(project_path)
        
        return project_path
    
    def _create_python_structure(self, project_path: str):
        """Crée la structure Python standard (models, services, utils, tests, resources)"""
        self.log_callback(f"📁 Création de la structure Python standard...")
        
        directories = ["models", "services", "utils", "tests", "resources"]
        for directory in directories:
            dir_path = os.path.join(project_path, directory)
            os.makedirs(dir_path, exist_ok=True)
            
            # Créer un __init__.py dans chaque dossier
            init_file = os.path.join(dir_path, "__init__.py")
            with open(init_file, "w") as f:
                f.write('"""Module {}"""\n'.format(directory))
        
        self.log_callback(f"✅ Structure créée : {', '.join(directories)}")
    
    def _copy_cursor_rules(self, project_path: str):
        """Copie le pack de règles Cursor depuis le template"""
        rules_source = os.path.expanduser("~/Developer/PYTHON/PROJETS/TEMPLATE/CursorRulesPack/cursor")
        cursor_dest = os.path.join(project_path, ".cursor")
        
        if os.path.isdir(rules_source):
            try:
                if os.path.exists(cursor_dest):
                    shutil.rmtree(cursor_dest)
                shutil.copytree(rules_source, cursor_dest)
                self.log_callback(f"✅ Pack de règles Cursor copié depuis TEMPLATE/CursorRulesPack")
            except Exception as e:
                self.log_callback(f"⚠️  Erreur lors de la copie des règles Cursor : {e}")
                # Créer un dossier .cursor/rules vide en cas d'erreur
                os.makedirs(os.path.join(project_path, ".cursor", "rules"), exist_ok=True)
        else:
            self.log_callback(f"⚠️  Pack CursorRulesPack introuvable dans {rules_source}")
            self.log_callback(f"💡 Les règles ne seront pas copiées. Création d'un dossier .cursor/rules vide.")
            # Créer un dossier .cursor/rules vide
            os.makedirs(os.path.join(project_path, ".cursor", "rules"), exist_ok=True)
    
    def _create_python_files(self, project_path: str, python_path: str):
        """Crée les fichiers Python de base"""
        
        # main.py - Utiliser un shebang robuste
        # Note: python_path peut contenir des espaces, donc on utilise python3 de manière générique
        main_content = '''#!/usr/bin/env python3
"""
Projet Python créé avec P_Creator
"""

def main():
    print("🚀 Bonjour depuis votre projet Python !")
    print("✅ Environnement virtuel activé automatiquement")

if __name__ == "__main__":
    main()
'''
        
        with open(os.path.join(project_path, "main.py"), "w") as f:
            f.write(main_content)
        
        # requirements.txt
        with open(os.path.join(project_path, "requirements.txt"), "w") as f:
            f.write("# Dépendances Python\n")
        
        # .gitignore
        gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
.venv/
venv/
ENV/
env/
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
        
        with open(os.path.join(project_path, ".gitignore"), "w") as f:
            f.write(gitignore_content)
        
        # README.md
        readme_content = f"""# {os.path.basename(project_path)}

Projet Python créé avec P_Creator.

## 🚀 Démarrage rapide

1. **Activez l'environnement virtuel :**
```bash
source .venv/bin/activate  # Linux/Mac
# ou
.venv\\Scripts\\activate   # Windows
```

2. **Installez les dépendances :**
```bash
pip install -r requirements.txt
```

3. **Lancez le projet :**
```bash
python main.py
```

## 📁 Structure

- `main.py` - Point d'entrée du projet
- `models/` - Modèles de données
- `services/` - Services métier
- `utils/` - Utilitaires
- `tests/` - Tests unitaires
- `resources/` - Ressources (configs, données, etc.)
- `requirements.txt` - Dépendances Python
- `.venv/` - Environnement virtuel
- `.gitignore` - Fichiers à ignorer par Git

## 🔧 Commandes utiles

```bash
# Activer l'environnement virtuel
source .venv/bin/activate

# Désactiver l'environnement virtuel
deactivate

# Installer une dépendance
pip install nom-package

# Sauvegarder les dépendances
pip freeze > requirements.txt
```
"""
        
        with open(os.path.join(project_path, "README.md"), "w") as f:
            f.write(readme_content)
    
    def _create_js_files(self, project_path: str):
        """Crée les fichiers JavaScript de base"""
        
        # index.js
        index_content = '''#!/usr/bin/env node
/**
 * Projet JavaScript créé avec P_Creator
 */

console.log("🚀 Bonjour depuis votre projet JavaScript !");
console.log("✅ Projet Node.js prêt !");

// Exemple de fonction
function greet(name = "Monde") {
    return `Bonjour, ${name} !`;
}

console.log(greet("Développeur"));
'''
        
        with open(os.path.join(project_path, "index.js"), "w") as f:
            f.write(index_content)
        
        # .gitignore
        gitignore_content = """# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Runtime data
pids
*.pid
*.seed
*.pid.lock

# Coverage directory used by tools like istanbul
coverage/

# nyc test coverage
.nyc_output

# Grunt intermediate storage
.grunt

# Bower dependency directory
bower_components

# node-waf configuration
.lock-wscript

# Compiled binary addons
build/Release

# Dependency directories
node_modules/
jspm_packages/

# Optional npm cache directory
.npm

# Optional REPL history
.node_repl_history

# Output of 'npm pack'
*.tgz

# Yarn Integrity file
.yarn-integrity

# dotenv environment variables file
.env

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db
"""
        
        with open(os.path.join(project_path, ".gitignore"), "w") as f:
            f.write(gitignore_content)
        
        # README.md
        readme_content = f"""# {os.path.basename(project_path)}

Projet JavaScript créé avec P_Creator.

## 🚀 Démarrage rapide

1. **Installez les dépendances :**
```bash
npm install
```

2. **Lancez le projet :**
```bash
npm start
```

## 📁 Structure

- `index.js` - Point d'entrée du projet
- `package.json` - Configuration et dépendances
- `.gitignore` - Fichiers à ignorer par Git

## 🔧 Commandes utiles

```bash
# Installer une dépendance
npm install nom-package

# Installer une dépendance de développement
npm install --save-dev nom-package

# Lancer le projet
npm start

# Lancer en mode développement
npm run dev
```
"""
        
        with open(os.path.join(project_path, "README.md"), "w") as f:
            f.write(readme_content)
    
    def _create_php_files(self, project_path: str):
        """Crée les fichiers PHP de base"""
        
        # index.php
        index_content = '''<?php
/**
 * Projet PHP créé avec P_Creator
 */

echo "🚀 Bonjour depuis votre projet PHP !\n";
echo "✅ Projet PHP prêt !\n";

// Exemple de fonction
function greet($name = "Monde") {
    return "Bonjour, $name !";
}

echo greet("Développeur") . "\n";
?>
'''
        
        with open(os.path.join(project_path, "index.php"), "w") as f:
            f.write(index_content)
        
        # .gitignore
        gitignore_content = """# PHP
vendor/
composer.lock

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log

# Cache
cache/
tmp/
"""
        
        with open(os.path.join(project_path, ".gitignore"), "w") as f:
            f.write(gitignore_content)
        
        # README.md
        readme_content = f"""# {os.path.basename(project_path)}

Projet PHP créé avec P_Creator.

## 🚀 Démarrage rapide

1. **Installez les dépendances :**
```bash
composer install
```

2. **Lancez le projet :**
```bash
php index.php
```

## 📁 Structure

- `index.php` - Point d'entrée du projet
- `composer.json` - Configuration et dépendances
- `.gitignore` - Fichiers à ignorer par Git

## 🔧 Commandes utiles

```bash
# Installer une dépendance
composer require vendor/package

# Installer une dépendance de développement
composer require --dev vendor/package

# Mettre à jour les dépendances
composer update

# Lancer le projet
php index.php
```
"""
        
        with open(os.path.join(project_path, "README.md"), "w") as f:
            f.write(readme_content)
    
    def _create_activation_script(self, project_path: str, venv_path: str):
        """Crée un script d'activation pour l'environnement virtuel"""
        
        if os.name == 'nt':  # Windows
            script_content = f"""@echo off
echo Activation de l'environnement virtuel...
call "{venv_path}\\Scripts\\activate.bat"
echo Environnement virtuel activé !
echo.
echo Commandes utiles:
echo   python main.py
echo   pip install -r requirements.txt
echo.
"""
            script_path = os.path.join(project_path, "activate.bat")
        else:  # Unix/Linux/macOS
            script_content = f"""#!/bin/bash
echo "🚀 Activation de l'environnement virtuel..."

# Vérifier si l'environnement virtuel existe
if [ ! -d "{venv_path}" ]; then
    echo "❌ Erreur : L'environnement virtuel n'existe pas dans {venv_path}"
    echo "💡 Créez-le avec : python3 -m venv .venv"
    exit 1
fi

# Activer l'environnement virtuel
source "{venv_path}/bin/activate"

# Vérifier l'activation
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ Environnement virtuel activé !"
    echo "📍 Chemin : $VIRTUAL_ENV"
    echo "🐍 Python : $(which python)"
    echo ""
    echo "🔧 Commandes utiles:"
    echo "  python main.py"
    echo "  pip install -r requirements.txt"
    echo "  pip list"
    echo ""
    echo "🚪 Pour désactiver : deactivate"
else
    echo "❌ Échec de l'activation de l'environnement virtuel"
    exit 1
fi
"""
            script_path = os.path.join(project_path, "activate.sh")
        
        with open(script_path, "w") as f:
            f.write(script_content)
        
        # Rendre le script exécutable sur Unix
        if os.name != 'nt':
            os.chmod(script_path, 0o755)
    
    def _create_check_script(self, project_path: str, venv_path: str):
        """Crée un script de vérification de l'environnement virtuel"""
        
        if os.name == 'nt':  # Windows
            script_content = f"""@echo off
echo 📊 État actuel de votre environnement
echo.

REM Vérifier si le dossier .venv existe
if exist "{venv_path}" (
    echo ✅ Le dossier .venv existe - Je le vois dans la liste des fichiers
) else (
    echo ❌ Le dossier .venv n'existe pas
    echo 💡 Créez-le avec : python -m venv .venv
    exit /b 1
)

REM Vérifier si l'environnement virtuel est activé
if defined VIRTUAL_ENV (
    echo ✅ L'environnement virtuel EST activé
    echo 📍 Chemin : %VIRTUAL_ENV%
    echo 🐍 Python : %VIRTUAL_ENV%\\Scripts\\python.exe
) else (
    echo ❌ L'environnement virtuel n'est PAS activé
    echo 💡 Activez-le avec : .venv\\Scripts\\activate.bat
)

echo.
echo 🚀 Pour activer votre environnement virtuel :
echo   .venv\\Scripts\\activate.bat
echo.
"""
            script_path = os.path.join(project_path, "check_env.bat")
        else:  # Unix/Linux/macOS
            script_content = f"""#!/bin/bash
echo "📊 État actuel de votre environnement"
echo ""

# Vérifier si le dossier .venv existe
if [ -d "{venv_path}" ]; then
    echo "✅ Le dossier .venv existe - Je le vois dans la liste des fichiers"
else
    echo "❌ Le dossier .venv n'existe pas"
    echo "💡 Créez-le avec : python3 -m venv .venv"
    exit 1
fi

# Vérifier si l'environnement virtuel est activé
if [ -n "$VIRTUAL_ENV" ]; then
    echo "✅ L'environnement virtuel EST activé"
    echo "📍 Chemin : $VIRTUAL_ENV"
    echo "🐍 Python : $(which python)"
else
    echo "❌ L'environnement virtuel n'est PAS activé - Voici les preuves :"
    echo "   \\$VIRTUAL_ENV est vide (pas de chemin affiché)"
    echo "   which python pointe vers $(which python) (Python système) au lieu du Python de l'environnement virtuel"
    echo ""
    echo "🚀 Pour activer votre environnement virtuel"
    echo "Vous avez deux options :"
    echo "Option 1 - Utiliser votre script d'activation :"
    echo "   ./activate.sh"
    echo "Option 2 - Activation manuelle :"
    echo "   source .venv/bin/activate"
    echo ""
    echo "🔍 Après activation, vous devriez voir :"
    echo "   Le prompt changera pour afficher (.venv) au début"
    echo "   La commande which python3 affichera quelque chose comme :"
    echo "   $VIRTUAL_ENV/bin/python3"
    echo "   La variable \\$VIRTUAL_ENV contiendra le chemin vers votre environnement"
fi

echo ""
"""
            script_path = os.path.join(project_path, "check_env.sh")
        
        with open(script_path, "w") as f:
            f.write(script_content)
        
        # Rendre le script exécutable sur Unix
        if os.name != 'nt':
            os.chmod(script_path, 0o755)
    
    def _activate_and_install_dependencies(self, project_path: str, venv_path: str, python_path: str):
        """Active l'environnement virtuel et installe les dépendances"""
        try:
            self.log_callback(f"🔧 Configuration de l'environnement virtuel...")
            
            # Mise à jour de pip via python -m pip (plus fiable)
            self.log_callback(f"📦 Mise à jour de pip...")
            subprocess.run([python_path, "-m", "pip", "install", "--upgrade", "pip"], 
                         check=True, cwd=project_path, timeout=120)
            
            # Installation des dépendances de base
            self.log_callback(f"📦 Installation des dépendances de base...")
            basic_deps = ["setuptools", "wheel"]
            for dep in basic_deps:
                subprocess.run([python_path, "-m", "pip", "install", dep], 
                             check=True, cwd=project_path, timeout=120)
            
            self.log_callback(f"✅ Environnement virtuel configuré !")
            self.log_callback(f"🎯 Votre projet est prêt à être utilisé !")
            
        except subprocess.CalledProcessError as e:
            self.log_callback(f"⚠️  Erreur lors de l'installation : {e}")
            self.log_callback(f"💡 Vous pouvez installer manuellement avec : source .venv/bin/activate && pip install -r requirements.txt")
        except subprocess.TimeoutExpired:
            self.log_callback(f"⚠️  Timeout lors de l'installation")
            self.log_callback(f"💡 Vous pouvez installer manuellement avec : source .venv/bin/activate && pip install -r requirements.txt")
        except Exception as e:
            self.log_callback(f"⚠️  Erreur inattendue : {e}")
            self.log_callback(f"💡 Vous pouvez installer manuellement avec : source .venv/bin/activate && pip install -r requirements.txt")

