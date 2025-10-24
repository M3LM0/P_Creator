#!/usr/bin/env python3
"""
P_Creator - Version Simplifiée
Créateur de projets avec environnement virtuel automatique
"""

import sys
import os
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QFileDialog, QMessageBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from services.language_manager import LanguageManager
from services.simple_generator import SimpleGenerator

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang_manager = LanguageManager()
        self.generator = SimpleGenerator(log_callback=self.log)
        self.last_created_project = None  # Chemin du dernier projet créé
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("P_Creator - Simple")
        self.setGeometry(100, 100, 600, 400)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # Titre
        title = QLabel("P_Creator - Créateur de Projets Simple")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Nom du projet
        layout.addWidget(QLabel("Nom du projet :"))
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("mon-projet")
        layout.addWidget(self.name_input)
        
        # Chemin du projet
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel("Chemin :"))
        self.path_input = QLineEdit(os.path.expanduser("~/Developer"))
        path_layout.addWidget(self.path_input)
        browse_btn = QPushButton("Parcourir")
        browse_btn.clicked.connect(self.browse_path)
        path_layout.addWidget(browse_btn)
        layout.addLayout(path_layout)
        
        # Langage
        layout.addWidget(QLabel("Langage :"))
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["Python", "JavaScript", "PHP"])
        self.lang_combo.currentTextChanged.connect(self.update_versions)
        layout.addWidget(self.lang_combo)
        
        # Version
        layout.addWidget(QLabel("Version :"))
        self.version_combo = QComboBox()
        self.version_combo.currentTextChanged.connect(self.update_status)
        layout.addWidget(self.version_combo)
        
        # Statut
        self.status_label = QLabel("Prêt")
        layout.addWidget(self.status_label)
        
        # Bouton de création
        self.create_btn = QPushButton("Créer le Projet")
        self.create_btn.clicked.connect(self.create_project)
        layout.addWidget(self.create_btn)
        
        # Bouton pour ouvrir dans Cursor (initialement caché)
        self.open_cursor_btn = QPushButton("🚀 Ouvrir dans Cursor")
        self.open_cursor_btn.clicked.connect(self.open_in_cursor)
        self.open_cursor_btn.setVisible(False)
        self.open_cursor_btn.setStyleSheet("""
            QPushButton {
                background-color: #007ACC;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #005A9E;
            }
        """)
        layout.addWidget(self.open_cursor_btn)
        
        # Bouton alternatif pour ouvrir le dossier (initialement caché)
        self.open_folder_btn = QPushButton("📁 Ouvrir le Dossier")
        self.open_folder_btn.clicked.connect(self.open_folder)
        self.open_folder_btn.setVisible(False)
        self.open_folder_btn.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
        """)
        layout.addWidget(self.open_folder_btn)
        
        # Console
        self.console = QTextEdit()
        self.console.setMaximumHeight(150)
        self.console.setReadOnly(True)
        layout.addWidget(self.console)
        
        # Initialisation
        self.update_versions()

    def browse_path(self):
        current_path = self.path_input.text()
        path = QFileDialog.getExistingDirectory(self, "Sélectionner le dossier", current_path)
        if path:
            self.path_input.setText(path)

    def update_versions(self):
        language = self.lang_combo.currentText()
        self.version_combo.clear()
        
        # Détecter les versions installées
        installed_versions = self.detect_installed_versions(language)
        
        # Ajouter l'indication d'installation
        versions_with_status = []
        for version in installed_versions:
            status = "✅" if version['installed'] else "❌"
            versions_with_status.append(f"{status} {version['version']}")
        
        self.version_combo.addItems(versions_with_status)
        
        # Mettre à jour le statut
        self.update_status()

    def detect_installed_versions(self, language):
        """Détecte les versions installées pour un langage donné"""
        versions = []
        
        if language == "Python":
            # Détecter via pyenv
            pyenv_versions = self.detect_pyenv_versions()
            # Détecter via brew
            brew_versions = self.detect_brew_python_versions()
            # Détecter via système
            system_versions = self.detect_system_python_versions()
            
            # Combiner toutes les versions trouvées
            all_versions = set()
            all_versions.update(pyenv_versions)
            all_versions.update(brew_versions)
            all_versions.update(system_versions)
            
            # Créer la liste avec statut d'installation
            for version in sorted(all_versions, reverse=True):
                versions.append({
                    'version': version,
                    'installed': True
                })
            
            # Ajouter les versions non installées pour référence
            common_versions = ["3.12", "3.11", "3.10", "3.9", "3.8"]
            for version in common_versions:
                if not any(v['version'] == version for v in versions):
                    versions.append({
                        'version': version,
                        'installed': False
                    })
        
        elif language == "JavaScript":
            # Détecter via nvm
            nvm_versions = self.detect_nvm_versions()
            # Détecter via système
            system_versions = self.detect_system_node_versions()
            
            all_versions = set()
            all_versions.update(nvm_versions)
            all_versions.update(system_versions)
            
            for version in sorted(all_versions, reverse=True):
                versions.append({
                    'version': version,
                    'installed': True
                })
            
            # Ajouter les versions communes
            common_versions = ["20", "18", "16", "14"]
            for version in common_versions:
                if not any(v['version'] == version for v in versions):
                    versions.append({
                        'version': version,
                        'installed': False
                    })
        
        elif language == "PHP":
            # Détecter via brew
            brew_versions = self.detect_brew_php_versions()
            # Détecter via système
            system_versions = self.detect_system_php_versions()
            
            all_versions = set()
            all_versions.update(brew_versions)
            all_versions.update(system_versions)
            
            for version in sorted(all_versions, reverse=True):
                versions.append({
                    'version': version,
                    'installed': True
                })
            
            # Ajouter les versions communes
            common_versions = ["8.3", "8.2", "8.1", "8.0"]
            for version in common_versions:
                if not any(v['version'] == version for v in versions):
                    versions.append({
                        'version': version,
                        'installed': False
                    })
        
        return versions

    def detect_pyenv_versions(self):
        """Détecte les versions Python installées via pyenv"""
        versions = []
        try:
            import subprocess
            result = subprocess.run(["pyenv", "versions", "--bare"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if line.strip():
                        # Extraire la version (ex: 3.9.24 -> 3.9)
                        version_parts = line.strip().split('.')
                        if len(version_parts) >= 2:
                            major_minor = f"{version_parts[0]}.{version_parts[1]}"
                            versions.append(major_minor)
        except:
            pass
        return versions

    def detect_brew_python_versions(self):
        """Détecte les versions Python installées via brew"""
        versions = []
        try:
            import subprocess
            result = subprocess.run(["brew", "list", "--formula"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if 'python@' in line:
                        version = line.replace('python@', '')
                        versions.append(version)
        except:
            pass
        return versions

    def detect_system_python_versions(self):
        """Détecte les versions Python du système"""
        versions = []
        try:
            import subprocess
            # Tester python3, python3.12, python3.11, etc.
            for version in ["3.12", "3.11", "3.10", "3.9", "3.8"]:
                try:
                    result = subprocess.run([f"python{version}", "--version"], 
                                         capture_output=True, text=True, timeout=5)
                    if result.returncode == 0:
                        versions.append(version)
                except:
                    pass
        except:
            pass
        return versions

    def detect_nvm_versions(self):
        """Détecte les versions Node.js installées via nvm"""
        versions = []
        try:
            import subprocess
            result = subprocess.run(["nvm", "list"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if 'v' in line and '.' in line:
                        # Extraire la version (ex: v20.10.0 -> 20)
                        version_match = line.split('v')[1].split('.')[0]
                        versions.append(version_match)
        except:
            pass
        return versions

    def detect_system_node_versions(self):
        """Détecte les versions Node.js du système"""
        versions = []
        try:
            import subprocess
            result = subprocess.run(["node", "--version"], 
                                 capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip().lstrip('v').split('.')[0]
                versions.append(version)
        except:
            pass
        return versions

    def detect_brew_php_versions(self):
        """Détecte les versions PHP installées via brew"""
        versions = []
        try:
            import subprocess
            result = subprocess.run(["brew", "list", "--formula"], 
                                 capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                for line in result.stdout.strip().split('\n'):
                    if 'php@' in line:
                        version = line.replace('php@', '')
                        versions.append(version)
        except:
            pass
        return versions

    def detect_system_php_versions(self):
        """Détecte les versions PHP du système"""
        versions = []
        try:
            import subprocess
            result = subprocess.run(["php", "--version"], 
                                 capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                version_line = result.stdout.split('\n')[0]
                # Extraire la version (ex: PHP 8.3.0 -> 8.3)
                if 'PHP' in version_line:
                    version_parts = version_line.split('PHP')[1].strip().split('.')
                    if len(version_parts) >= 2:
                        major_minor = f"{version_parts[0]}.{version_parts[1]}"
                        versions.append(major_minor)
        except:
            pass
        return versions

    def check_language_installation(self, language, version):
        """Vérifie si une version de langage est installée"""
        try:
            if language == "Python":
                import subprocess
                result = subprocess.run([f"python{version}", "--version"], 
                                     capture_output=True, text=True, timeout=5)
                return result.returncode == 0
            elif language == "JavaScript":
                import subprocess
                result = subprocess.run(["node", "--version"], 
                                     capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    # Vérifier si la version correspond
                    installed_version = result.stdout.strip().lstrip('v')
                    major_version = installed_version.split('.')[0]
                    return major_version == version
                return False
            elif language == "PHP":
                import subprocess
                result = subprocess.run(["php", "--version"], 
                                     capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    # Vérifier si la version correspond
                    version_line = result.stdout.split('\n')[0]
                    if f"PHP {version}" in version_line:
                        return True
                return False
        except:
            return False
        return False

    def update_status(self):
        """Met à jour le statut d'installation"""
        if self.version_combo.count() > 0:
            current_text = self.version_combo.currentText()
            if "✅" in current_text:
                self.status_label.setText("✅ Langage installé")
                self.status_label.setStyleSheet("color: green; font-weight: bold;")
            else:
                self.status_label.setText("❌ Langage non installé")
                self.status_label.setStyleSheet("color: red; font-weight: bold;")
        else:
            self.status_label.setText("Prêt")
            self.status_label.setStyleSheet("")

    def create_project(self):
        name = self.name_input.text().strip()
        path = self.path_input.text().strip()
        language = self.lang_combo.currentText()
        version_text = self.version_combo.currentText()
        
        # Extraire la version sans les emojis
        version = version_text.replace("✅ ", "").replace("❌ ", "")
        
        if not name:
            QMessageBox.warning(self, "Erreur", "Veuillez saisir un nom de projet")
            return
        
        if not path:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner un chemin")
            return
        
        try:
            # Cacher les boutons d'ouverture si on crée un nouveau projet
            self.open_cursor_btn.setVisible(False)
            self.open_folder_btn.setVisible(False)
            
            self.log(f"🚀 Création du projet '{name}'...")
            self.log(f"📁 Chemin : {path}")
            self.log(f"🔧 Langage : {language} {version}")
            self.log("=" * 50)
            
            # Création du projet
            project_path = self.generator.create_project(
                name=name,
                path=path,
                language=language,
                version=version
            )
            
            self.log("=" * 50)
            self.log(f"✅ Projet créé avec succès !")
            self.log(f"📂 Dossier : {project_path}")
            self.log(f"🎯 Votre projet est prêt à être utilisé !")
            
            # Stocker le chemin du projet créé
            self.last_created_project = project_path
            
            # Afficher les boutons d'ouverture
            self.open_cursor_btn.setVisible(True)
            self.open_cursor_btn.setText(f"🚀 Ouvrir '{name}' dans Cursor")
            self.open_folder_btn.setVisible(True)
            self.open_folder_btn.setText(f"📁 Ouvrir le dossier '{name}'")
            
            # Message de succès
            QMessageBox.information(
                self, 
                "Succès", 
                f"Projet '{name}' créé avec succès !\n\n"
                f"Chemin : {project_path}\n\n"
                f"Cliquez sur le bouton 'Ouvrir dans Cursor' pour commencer à coder !"
            )
            
        except Exception as e:
            self.log("=" * 50)
            self.log(f"❌ Erreur : {str(e)}")
            QMessageBox.critical(self, "Erreur", f"Erreur lors de la création :\n{str(e)}")

    def open_in_cursor(self):
        """Ouvre Cursor dans le dossier du projet créé avec gestion d'erreurs améliorée"""
        if not self.last_created_project:
            QMessageBox.warning(self, "Erreur", "Aucun projet créé récemment")
            return
        
        try:
            import subprocess
            import platform
            import time
            
            self.log(f"🚀 Ouverture de Cursor dans : {self.last_created_project}")
            
            # Détecter l'OS et utiliser la bonne commande
            system = platform.system()
            success = False
            
            if system == "Darwin":  # macOS
                # Méthode 1: Commande cursor (si installé via npm)
                try:
                    self.log("🔍 Tentative avec la commande 'cursor'...")
                    result = subprocess.run(
                        ["cursor", self.last_created_project], 
                        check=True, 
                        timeout=10,
                        capture_output=True,
                        text=True
                    )
                    self.log("✅ Cursor ouvert avec succès (commande cursor) !")
                    success = True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
                    self.log(f"⚠️  Commande 'cursor' échouée : {str(e)}")
                    
                    # Méthode 2: Ouvrir avec l'application Cursor
                    try:
                        self.log("🔍 Tentative avec l'application Cursor...")
                        subprocess.run(
                            ["open", "-a", "Cursor", self.last_created_project], 
                            check=True,
                            timeout=10
                        )
                        self.log("✅ Cursor ouvert avec succès (application) !")
                        success = True
                    except (subprocess.CalledProcessError, subprocess.TimeoutExpired) as e2:
                        self.log(f"⚠️  Application Cursor échouée : {str(e2)}")
                        
                        # Méthode 3: Ouvrir le dossier dans le Finder
                        try:
                            self.log("🔍 Ouverture du dossier dans le Finder...")
                            subprocess.run(["open", self.last_created_project], check=True)
                            self.log("✅ Dossier ouvert dans le Finder !")
                            self.log("💡 Vous pouvez maintenant glisser-déposer le dossier dans Cursor")
                            success = True
                        except Exception as e3:
                            self.log(f"❌ Impossible d'ouvrir le dossier : {str(e3)}")
            
            elif system == "Windows":
                # Windows
                try:
                    subprocess.run(["cursor", self.last_created_project], check=True, timeout=10)
                    self.log("✅ Cursor ouvert avec succès !")
                    success = True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    # Fallback: ouvrir le dossier dans l'explorateur
                    subprocess.run(["explorer", self.last_created_project], check=True)
                    self.log("✅ Dossier ouvert dans l'Explorateur !")
                    success = True
            
            else:  # Linux
                try:
                    subprocess.run(["cursor", self.last_created_project], check=True, timeout=10)
                    self.log("✅ Cursor ouvert avec succès !")
                    success = True
                except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired):
                    # Fallback: ouvrir le dossier dans le gestionnaire de fichiers
                    subprocess.run(["xdg-open", self.last_created_project], check=True)
                    self.log("✅ Dossier ouvert dans le gestionnaire de fichiers !")
                    success = True
            
            if success:
                # Masquer le bouton après utilisation
                self.open_cursor_btn.setVisible(False)
                
                # Afficher un message d'aide
                QMessageBox.information(
                    self,
                    "Projet ouvert",
                    "Le projet a été ouvert !\n\n"
                    "Si Cursor ne s'est pas ouvert automatiquement :\n"
                    "1. Ouvrez Cursor manuellement\n"
                    "2. Utilisez File > Open Folder\n"
                    "3. Sélectionnez le dossier du projet"
                )
            else:
                raise Exception("Toutes les méthodes d'ouverture ont échoué")
            
        except FileNotFoundError:
            self.log("❌ Cursor n'est pas installé ou pas dans le PATH")
            QMessageBox.warning(
                self, 
                "Cursor non trouvé", 
                "Cursor n'est pas installé ou pas dans le PATH.\n\n"
                "Solutions :\n"
                "1. Installez Cursor depuis : https://cursor.sh/\n"
                "2. Ou ouvrez manuellement le dossier :\n" + self.last_created_project
            )
        except Exception as e:
            self.log(f"❌ Erreur lors de l'ouverture : {str(e)}")
            QMessageBox.critical(
                self, 
                "Erreur", 
                f"Impossible d'ouvrir Cursor automatiquement.\n\n"
                f"Solutions manuelles :\n"
                f"1. Ouvrez Cursor\n"
                f"2. File > Open Folder\n"
                f"3. Sélectionnez : {self.last_created_project}\n\n"
                f"Ou copiez ce chemin :\n{self.last_created_project}"
            )

    def open_folder(self):
        """Ouvre le dossier du projet dans le gestionnaire de fichiers"""
        if not self.last_created_project:
            QMessageBox.warning(self, "Erreur", "Aucun projet créé récemment")
            return
        
        try:
            import subprocess
            import platform
            
            self.log(f"📁 Ouverture du dossier : {self.last_created_project}")
            
            system = platform.system()
            
            if system == "Darwin":  # macOS
                subprocess.run(["open", self.last_created_project], check=True)
                self.log("✅ Dossier ouvert dans le Finder !")
                self.log("💡 Vous pouvez maintenant glisser-déposer le dossier dans Cursor")
            elif system == "Windows":
                subprocess.run(["explorer", self.last_created_project], check=True)
                self.log("✅ Dossier ouvert dans l'Explorateur !")
            else:  # Linux
                subprocess.run(["xdg-open", self.last_created_project], check=True)
                self.log("✅ Dossier ouvert dans le gestionnaire de fichiers !")
            
            # Masquer le bouton après utilisation
            self.open_folder_btn.setVisible(False)
            
            QMessageBox.information(
                self,
                "Dossier ouvert",
                "Le dossier du projet a été ouvert !\n\n"
                "Pour ouvrir dans Cursor :\n"
                "1. Glissez-déposez le dossier dans Cursor\n"
                "2. Ou utilisez File > Open Folder dans Cursor"
            )
            
        except Exception as e:
            self.log(f"❌ Erreur lors de l'ouverture du dossier : {str(e)}")
            QMessageBox.critical(
                self,
                "Erreur",
                f"Impossible d'ouvrir le dossier :\n{str(e)}\n\n"
                f"Chemin du projet :\n{self.last_created_project}"
            )

    def log(self, message):
        self.console.append(message)
        self.console.ensureCursorVisible()

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("P_Creator Simple")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()