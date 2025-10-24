import subprocess
import os
from services.language_manager import LanguageManager

class PythonGenerator:
    """
    Génère un projet Python avec l'interpréteur exact sélectionné (ex: /opt/homebrew/bin/python3.12 ou ~/.pyenv/versions/3.9.24/bin/python3)
    """

    def preview_structure(self, ctx):
        return {
            "dirs": ["src", "tests"],
            "files": ["README.md", "requirements.txt", ".gitignore"]
        }

    def generate(self, ctx):
        project_path = os.path.join(ctx["base_path"], ctx["name"])
        os.makedirs(project_path, exist_ok=True)

        # Récupération du bon interpréteur Python
        lang = "Python"
        version = ctx["lang_version"]
        python_path = LanguageManager.get_installation_path(lang, version)

        if not python_path or not os.path.exists(python_path):
            raise RuntimeError(f"Python {version} introuvable sur le système.\nChemin recherché : {python_path}")

        print(f"🧩 Utilisation de l'interpréteur : {python_path}")

        # Création de l'environnement virtuel avec le bon binaire
        venv_path = os.path.join(project_path, ".venv")
        try:
            subprocess.run([python_path, "-m", "venv", venv_path], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Erreur lors de la création du venv : {e}")

        # Fichiers initiaux
        with open(os.path.join(project_path, "README.md"), "w") as f:
            f.write(f"# Projet {ctx['name']}\n\nCréé avec Python {version} ({python_path})\n")

        with open(os.path.join(project_path, ".gitignore"), "w") as f:
            f.write(".venv/\n__pycache__/\n*.pyc\n")

        open(os.path.join(project_path, "requirements.txt"), "a").close()
        os.makedirs(os.path.join(project_path, "src"), exist_ok=True)
        os.makedirs(os.path.join(project_path, "tests"), exist_ok=True)

        print(f"✅ Projet {ctx['name']} créé avec succès dans {project_path}")
        return project_path