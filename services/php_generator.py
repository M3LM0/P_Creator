import os
from .generator_base import ProjectGeneratorBase
from .utils import run_cmd

README = "(PHP Project)\n"
GITIGNORE = ["vendor/", "node_modules/", ".env"]

class PHPGenerator(ProjectGeneratorBase):
    def preview_structure(self, ctx):
        return {
            "dirs": ["public", "src"],
            "files": ["composer.json", ".gitignore", "README.md"]
        }

    def generate(self, ctx):
        project_path = os.path.join(ctx["base_path"], ctx["name"])
        os.makedirs(project_path, exist_ok=True)

        self.make_tree(
            project_path,
            dirs=["public", "src"],
            files={
                "composer.json": '{\n  "name": "user/project",\n  "require": {}\n}\n',
                ".gitignore": "\n".join(GITIGNORE) + "\n",
                "README.md": f"# {ctx['name']} {README}"
            }
        )

        # Composer install si disponible (crée vendor/)
        run_cmd(["composer", "install"], cwd=project_path)

        return project_path