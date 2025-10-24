import os
from PySide6.QtWidgets import (
    QWidget, QLabel, QLineEdit, QPushButton, QComboBox,
    QFileDialog, QMessageBox, QHBoxLayout, QVBoxLayout,
    QSplitter, QProgressBar, QPlainTextEdit
)
from PySide6.QtCore import Qt, QThread, Signal

from ui.preview_tree import PreviewTree
from services.language_manager import LanguageManager
from services.python_generator import PythonGenerator
from services.php_generator import PHPGenerator
from services.js_generator import JSGenerator

LANGS = {
    "Python": PythonGenerator,
    "PHP": PHPGenerator,
    "JavaScript": JSGenerator,
}

class InstallThread(QThread):
    progress = Signal(str)
    finished = Signal(bool)

    def __init__(self, lang, version):
        super().__init__()
        self.lang = lang
        self.version = version

    def run(self):
        manager = LanguageManager()
        self.progress.emit(f"🚀 Installation de {self.lang} {self.version}...\n")
        ok = manager.install_version(self.lang, self.version)
        self.finished.emit(ok)
        if ok:
            self.progress.emit(f"✅ {self.lang} {self.version} installé.\n")
        else:
            self.progress.emit(f"❌ Échec de l'installation.\n")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.lang_manager = LanguageManager()
        self.install_thread = None
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Universal Project Creator - V5.1")
        self.resize(1200, 720)

        # Nom + chemin
        self.name_label = QLabel("Nom du projet :")
        self.name_input = QLineEdit()
        self.name_input.textChanged.connect(self.update_preview)

        self.path_label = QLabel("Chemin du projet :")
        default_path = os.path.expanduser("~/Developer/PROJETS")
        self.path_input = QLineEdit(default_path)
        self.browse_btn = QPushButton("Parcourir…")
        self.browse_btn.clicked.connect(self.choose_folder)

        # Langage + version
        self.lang_label = QLabel("Langage :")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(list(LANGS.keys()))
        self.lang_combo.currentIndexChanged.connect(self.update_versions)

        self.version_label = QLabel("Version :")
        self.version_combo = QComboBox()
        self.version_combo.currentIndexChanged.connect(self.update_install_status)

        self.status_label = QLabel("⏳ Vérification en cours…")
        self.status_label.setStyleSheet("color: gray; font-style: italic;")

        self.install_btn = QPushButton("Installer cette version")
        self.install_btn.clicked.connect(self.install_selected_version)

        self.create_btn = QPushButton("Créer le projet")
        self.create_btn.clicked.connect(self.create_project)

        # Progression & console
        self.progress_bar = QProgressBar()
        self.console = QPlainTextEdit()
        self.console.setReadOnly(True)

        # Layout gauche
        path_layout = QHBoxLayout()
        path_layout.addWidget(self.path_input)
        path_layout.addWidget(self.browse_btn)

        version_layout = QHBoxLayout()
        version_layout.addWidget(self.version_combo)
        version_layout.addWidget(self.install_btn)

        left = QVBoxLayout()
        left.addWidget(self.name_label)
        left.addWidget(self.name_input)
        left.addWidget(self.path_label)
        left.addLayout(path_layout)
        left.addWidget(self.lang_label)
        left.addWidget(self.lang_combo)
        left.addWidget(self.version_label)
        left.addLayout(version_layout)
        left.addWidget(self.status_label)
        left.addWidget(self.create_btn)
        left.addWidget(QLabel("Progression :"))
        left.addWidget(self.progress_bar)
        left.addWidget(QLabel("Console :"))
        left.addWidget(self.console)
        left.addStretch()

        left_widget = QWidget()
        left_widget.setLayout(left)

        # Prévisualisation
        self.preview = PreviewTree()
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(self.preview)
        splitter.setSizes([500, 700])

        layout = QHBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)

        # Initialisation
        self.update_versions()
        self.update_preview()

    # --- Fonctions principales ---
    def update_versions(self):
        lang = self.lang_combo.currentText()
        versions = self.lang_manager.detect_versions(lang)
        self.version_combo.clear()
        self.version_combo.addItems(versions)
        self.update_install_status()
        self.update_preview()

    def update_install_status(self):
        lang = self.lang_combo.currentText()
        version = self.version_combo.currentText()
        path = self.lang_manager.get_installation_path(lang, version)
        if path:
            self.status_label.setText(f"✅ Installé : {path}")
            self.status_label.setStyleSheet("color: green;")
        else:
            self.status_label.setText("❌ Non installé")
            self.status_label.setStyleSheet("color: red;")

    def install_selected_version(self):
        lang = self.lang_combo.currentText()
        version = self.version_combo.currentText()

        if self.lang_manager.is_version_installed(lang, version):
            QMessageBox.information(self, "Info", f"{lang} {version} est déjà installé.")
            return

        self.progress_bar.setValue(0)
        self.console.clear()

        self.install_thread = InstallThread(lang, version)
        self.install_thread.progress.connect(self.append_log)
        self.install_thread.finished.connect(self.install_done)
        self.install_thread.start()

    def append_log(self, text):
        self.console.appendPlainText(text)
        self.progress_bar.setValue(min(95, self.progress_bar.value() + 5))

    def install_done(self, ok):
        self.progress_bar.setValue(100 if ok else 0)
        self.update_install_status()

    def choose_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Choisir un dossier")
        if folder:
            self.path_input.setText(folder)
            self.update_preview()

    def current_generator(self):
        lang = self.lang_combo.currentText()
        return LANGS[lang]()

    def current_context(self):
        return {
            "name": self.name_input.text().strip() or "nouveau_projet",
            "base_path": self.path_input.text().strip(),
            "lang_version": self.version_combo.currentText()
        }

    def create_project(self):
        gen = self.current_generator()
        ctx = self.current_context()
        try:
            project_path = gen.generate(ctx)
            QMessageBox.information(self, "Succès", f"Projet créé : {project_path}")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", str(e))

    def update_preview(self):
        gen = self.current_generator()
        ctx = self.current_context()
        structure = gen.preview_structure(ctx)
        self.preview.render(ctx["name"], structure)