import os
from .generator_base import ProjectGeneratorBase
from .utils import run_cmd

README = "(JavaScript Project)\n"
GITIGNORE = ["node_modules/", "dist/", ".env"]

class JSGenerator(ProjectGeneratorBase):
    def preview_structure(self, ctx):
        return {
            "dirs": ["src"],
            "files": ["package.json", ".gitignore", "README.md"]
        }

    def generate(self, ctx):
        project_path = os.path.join(ctx["base_path"], ctx["name"])
        os.makedirs(project_path, exist_ok=True)

        pkg = (
            '{\n'
            f'  "name": "{ctx["name"]}",\n'
            '  "version": "1.0.0",\n'
            '  "scripts": {\n'
            '    "dev": "node index.js || vite",\n'
            '    "build": "echo \\"add your bundler\\""\n'
            '  }\n'
            '}\n'
        )

        self.make_tree(
            project_path,
            dirs=["src"],
            files={
                "package.json": pkg,
                ".gitignore": "\n".join(GITIGNORE) + "\n",
                "README.md": f"# {ctx['name']} {README}",
                "src/index.js": 'console.log("Hello JS Project");\n'
            }
        )

        # npm install (créera node_modules s’il y a des deps)
        run_cmd(["npm", "install"], cwd=project_path)

        return project_path