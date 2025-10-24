import os
from abc import ABC, abstractmethod
from .utils import ensure_dirs, write_file, run_cmd

class ProjectGeneratorBase(ABC):
    @abstractmethod
    def preview_structure(self, ctx) -> dict:
        """Retourne {'dirs': [...], 'files': [...]} pour l'aperçu."""
        ...

    @abstractmethod
    def generate(self, ctx) -> str:
        """Génère le projet sur disque. Retourne le chemin du projet."""
        ...

    # Helpers communs
    def create_common_files(self, project_path: str, readme_title: str, gitignore_lines):
        write_file(os.path.join(project_path, "README.md"), f"# {readme_title}\n")
        write_file(os.path.join(project_path, ".gitignore"), "\n".join(gitignore_lines) + "\n")

    def make_tree(self, base: str, dirs: list, files: dict):
        ensure_dirs([os.path.join(base, d) for d in dirs])
        for rel, content in files.items():
            write_file(os.path.join(base, rel), content)