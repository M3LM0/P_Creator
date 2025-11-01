import subprocess
import shutil
import os
import re

class LanguageManager:
    SUPPORTED = {
        "Python": ["3.9", "3.10", "3.11", "3.12", "3.13"],
        "PHP": ["8.1", "8.2", "8.3"],
        "JavaScript": ["Node 18", "Node 20", "Node 22"]
    }
    
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
                # Normaliser la version
                normalized_version = LanguageManager._normalize_python_version(version)
                
                # Essayer plusieurs méthodes pour détecter Python
                python_commands = [
                    f"python{version}",           # python3.9.24
                    f"python{normalized_version}", # python3.9
                    "python3",                    # python3 (version par défaut)
                    "python"                     # python (version par défaut)
                ]
                
                for cmd in python_commands:
                    try:
                        result = subprocess.run([cmd, "--version"], 
                                              capture_output=True, text=True, timeout=5)
                        if result.returncode == 0:
                            # Combiner stdout et stderr pour la détection
                            output = (result.stdout or '') + (result.stderr or '')
                            # Vérifier que la version correspond
                            if normalized_version in output or version in output:
                                return True
                    except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                        continue
                
                # Vérifier avec le chemin complet si disponible
                full_path = LanguageManager.get_installation_path(lang, version)
                if full_path and os.path.exists(full_path):
                    try:
                        result = subprocess.run([full_path, "--version"], 
                                              capture_output=True, text=True, timeout=5)
                        return result.returncode == 0
                    except:
                        pass
                
                return False
                
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
    def get_installation_path(lang, version):
        """Retourne le chemin complet du binaire si la version est installée, sinon None."""
        try:
            if lang == "Python":
                # Normaliser la version
                normalized_version = LanguageManager._normalize_python_version(version)
                
                # 1️⃣ Vérifie dans Homebrew
                brew_bin = f"/opt/homebrew/bin/python{normalized_version}"
                if os.path.exists(brew_bin):
                    return brew_bin

                # 2️⃣ Vérifie dans pyenv
                pyenv_root = os.path.expanduser("~/.pyenv/versions")
                if os.path.isdir(pyenv_root):
                    for v in os.listdir(pyenv_root):
                        if v.startswith(normalized_version) or v.startswith(version):
                            bin_path = os.path.join(pyenv_root, v, "bin", "python")
                            if os.path.exists(bin_path):
                                return bin_path

                # 3️⃣ Vérifie dans /usr/local/bin
                usr_bin = f"/usr/local/bin/python{normalized_version}"
                if os.path.exists(usr_bin):
                    return usr_bin

                # 4️⃣ Vérifie dans le PATH
                path = shutil.which(f"python{normalized_version}")
                if path:
                    return path
                
                # 5️⃣ Essayer aussi avec la version complète
                path = shutil.which(f"python{version}")
                if path:
                    return path

                return None

            elif lang == "PHP":
                return shutil.which("php")

            elif lang == "JavaScript":
                return shutil.which("node")

        except Exception:
            return None