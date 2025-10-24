from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

class PreviewTree(QTreeWidget):
    def __init__(self):
        super().__init__()
        self.setHeaderLabel("Aperçu du projet")
        self.setColumnCount(1)

    def render(self, project_name: str, structure: dict):
        self.clear()
        root = QTreeWidgetItem([project_name])
        self.addTopLevelItem(root)

        for d in structure.get("dirs", []):
            QTreeWidgetItem(root, [d if d.endswith("/") else f"{d}/"])
        for f in structure.get("files", []):
            QTreeWidgetItem(root, [f])

        self.expandAll()