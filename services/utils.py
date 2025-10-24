import os
import shutil
import subprocess

def ensure_dirs(paths):
    for p in paths:
        os.makedirs(p, exist_ok=True)

def write_file(path: str, content: str):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def run_cmd(cmd, cwd=None, check=False):
    """Exécute une commande si l'exécutable existe. Retourne (ok:bool, CompletedProcess|None)."""
    exe = cmd[0]
    if shutil.which(exe) is None:
        return False, None
    try:
        cp = subprocess.run(cmd, cwd=cwd, check=check)
        return cp.returncode == 0, cp
    except Exception:
        return False, None