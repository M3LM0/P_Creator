import subprocess
import shutil
import os

class LanguageManager:
    SUPPORTED = {
        "Python": ["3.9", "3.10", "3.11", "3.12", "3.13"],
        "PHP": ["8.1", "8.2", "8.3"],
        "JavaScript": ["Node 18", "Node 20", "Node 22"]
    }

    @staticmethod
    def _run(cmd, shell=False):
        try:
            subprocess.run(cmd, shell=shell, check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    @staticmethod
    def detect_versions(lang):
        versions = []
        try:
            if lang == "Python" and shutil.which("pyenv"):
                output = subprocess.check_output(["pyenv", "versions", "--bare"], text=True)
                versions = [v.strip() for v in output.splitlines() if v.strip()]
            elif lang == "PHP" and shutil.which("php"):
                output = subprocess.check_output(["php", "-v"], text=True)
                versions = [output.split()[1].split('-')[0]]
            elif lang == "JavaScript" and shutil.which("node"):
                output = subprocess.check_output(["node", "-v"], text=True).strip()
                versions = [output.replace("v", "Node ")]
        except Exception:
            pass
        default_versions = LanguageManager.SUPPORTED.get(lang, [])
        return sorted(set(default_versions + versions))

    @staticmethod
    def is_version_installed(lang, version):
        try:
            if lang == "Python":
                result = subprocess.run(["python" + version[:3], "--version"], capture_output=True)
                return result.returncode == 0
            elif lang == "PHP":
                if shutil.which("php"):
                    out = subprocess.check_output(["php", "-v"], text=True)
                    return version.split('.')[0] in out
            elif lang == "JavaScript":
                if shutil.which("node"):
                    out = subprocess.check_output(["node", "-v"], text=True)
                    return version.split()[1] in out
        except Exception:
            return False
        return False

    @staticmethod
    def install_version(lang, version):
        print(f"🛠 Installation de {lang} {version}...")
        try:
            if lang == "Python":
                LanguageManager.ensure_pyenv()
                LanguageManager._run(["pyenv", "install", "-s", version])
            elif lang == "PHP":
                LanguageManager.ensure_brew()
                LanguageManager._run(["brew", "install", f"php@{version}"])
            elif lang == "JavaScript":
                LanguageManager.ensure_nvm()
                ver_num = version.split()[1]
                LanguageManager._run(f"source ~/.nvm/nvm.sh && nvm install {ver_num}", shell=True)
                LanguageManager._run(f"source ~/.nvm/nvm.sh && nvm alias default {ver_num}", shell=True)
            print(f"✅ {lang} {version} installé.")
            return True
        except Exception as e:
            print("❌ Erreur d'installation :", e)
            return False

    @staticmethod
    def ensure_brew():
        if not shutil.which("brew"):
            print("➡️ Installation de Homebrew…")
            subprocess.run(
                '/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"',
                shell=True, check=False)
            os.environ["PATH"] += ":/opt/homebrew/bin"
        else:
            print("✅ Homebrew déjà installé.")

    @staticmethod
    def ensure_pyenv():
        if not shutil.which("pyenv"):
            LanguageManager.ensure_brew()
            print("➡️ Installation de pyenv…")
            LanguageManager._run(["brew", "install", "pyenv"])
        else:
            print("✅ pyenv déjà installé.")

    @staticmethod
    def ensure_nvm():
        nvm_path = os.path.expanduser("~/.nvm/nvm.sh")
        if not shutil.which("nvm") and not os.path.exists(nvm_path):
            print("➡️ Installation de nvm…")
            subprocess.run(
                'curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.7/install.sh | bash',
                shell=True, check=False)
        else:
            print("✅ nvm déjà installé.")

    @staticmethod
    def get_installation_path(lang, version):
        """Retourne le chemin complet du binaire si la version est installée, sinon None."""
        try:
            if lang == "Python":
                # 1️⃣ Vérifie dans Homebrew
                brew_bin = f"/opt/homebrew/bin/python{version[:3]}"
                if os.path.exists(brew_bin):
                    return brew_bin

                # 2️⃣ Vérifie dans pyenv
                pyenv_root = os.path.expanduser("~/.pyenv/versions")
                if os.path.isdir(pyenv_root):
                    for v in os.listdir(pyenv_root):
                        if v.startswith(version):
                            bin_path = os.path.join(pyenv_root, v, "bin", "python")
                            if os.path.exists(bin_path):
                                return bin_path

                # 3️⃣ Vérifie dans /usr/local/bin
                usr_bin = f"/usr/local/bin/python{version[:3]}"
                if os.path.exists(usr_bin):
                    return usr_bin

                # 4️⃣ Vérifie dans le PATH
                path = shutil.which(f"python{version[:3]}")
                if path:
                    return path

                return None

            elif lang == "PHP":
                return shutil.which("php")

            elif lang == "JavaScript":
                return shutil.which("node")

        except Exception:
            return None