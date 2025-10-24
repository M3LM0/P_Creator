"""
Générateur simple pour P_Creator
Crée des projets basiques avec environnement virtuel automatique
"""

import os
import subprocess
from typing import Dict, List

class SimpleGenerator:
    """Générateur simple de projets"""
    
    def __init__(self, log_callback=None):
        self.supported_languages = ["Python", "JavaScript", "PHP"]
        self.log_callback = log_callback or print
    
    def create_project(self, name: str, path: str, language: str, version: str) -> str:
        """
        Crée un projet simple avec environnement virtuel
        
        Args:
            name: Nom du projet
            path: Chemin de base
            language: Langage de programmation
            version: Version du langage
            
        Returns:
            Chemin complet du projet créé
        """
        # Chemin complet du projet
        project_path = os.path.join(path, name)
        
        # Création du dossier
        os.makedirs(project_path, exist_ok=True)
        
        if language == "Python":
            return self._create_python_project(project_path, version)
        elif language == "JavaScript":
            return self._create_js_project(project_path, version)
        elif language == "PHP":
            return self._create_php_project(project_path, version)
        else:
            raise ValueError(f"Langage non supporté : {language}")
    
    def _create_python_project(self, project_path: str, version: str) -> str:
        """Crée un projet Python avec environnement virtuel"""
        self.log_callback(f"🐍 Création du projet Python {version}...")
        
        # Création de l'environnement virtuel
        venv_path = os.path.join(project_path, ".venv")
        python_cmd = f"python{version}"
        
        try:
            subprocess.run([python_cmd, "-m", "venv", venv_path], check=True)
            self.log_callback(f"✅ Environnement virtuel créé : {venv_path}")
        except subprocess.CalledProcessError:
            # Fallback sur python3 si python{version} n'existe pas
            subprocess.run(["python3", "-m", "venv", venv_path], check=True)
            self.log_callback(f"✅ Environnement virtuel créé (fallback python3) : {venv_path}")
        
        # Détermination du pip selon l'OS
        if os.name == 'nt':  # Windows
            pip_path = os.path.join(venv_path, "Scripts", "pip.exe")
            python_path = os.path.join(venv_path, "Scripts", "python.exe")
        else:  # Unix/Linux/macOS
            pip_path = os.path.join(venv_path, "bin", "pip")
            python_path = os.path.join(venv_path, "bin", "python")
        
        # Création des fichiers de base
        self._create_python_files(project_path, python_path)
        
        # Création du script d'activation
        self._create_activation_script(project_path, venv_path)
        
        # Création du script de vérification
        self._create_check_script(project_path, venv_path)
        
        # Activation automatique et installation des dépendances
        self._activate_and_install_dependencies(project_path, venv_path, pip_path)
        
        return project_path
    
    def _create_js_project(self, project_path: str, version: str) -> str:
        """Crée un projet JavaScript avec package.json"""
        self.log_callback(f"🟨 Création du projet JavaScript Node.js {version}...")
        
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
                "node": f">={version}.0.0"
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
    
    def _create_python_files(self, project_path: str, python_path: str):
        """Crée les fichiers Python de base"""
        
        # main.py
        main_content = f'''#!/usr/bin/env {python_path}
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
    
    def _activate_and_install_dependencies(self, project_path: str, venv_path: str, pip_path: str):
        """Active l'environnement virtuel et installe les dépendances"""
        try:
            self.log_callback(f"🔧 Activation de l'environnement virtuel...")
            
            # Mise à jour de pip
            self.log_callback(f"📦 Mise à jour de pip...")
            subprocess.run([pip_path, "install", "--upgrade", "pip"], 
                         check=True, cwd=project_path)
            
            # Installation des dépendances de base
            self.log_callback(f"📦 Installation des dépendances de base...")
            basic_deps = ["setuptools", "wheel"]
            for dep in basic_deps:
                subprocess.run([pip_path, "install", dep], 
                             check=True, cwd=project_path)
            
            self.log_callback(f"✅ Environnement virtuel activé et configuré !")
            self.log_callback(f"🎯 Votre projet est prêt à être utilisé !")
            
        except subprocess.CalledProcessError as e:
            self.log_callback(f"⚠️  Erreur lors de l'activation : {e}")
            self.log_callback(f"💡 Vous pouvez activer manuellement avec : source .venv/bin/activate")
        except Exception as e:
            self.log_callback(f"⚠️  Erreur inattendue : {e}")
            self.log_callback(f"💡 Vous pouvez activer manuellement avec : source .venv/bin/activate")

