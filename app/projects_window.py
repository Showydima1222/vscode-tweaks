from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QListWidget, 
                             QPushButton, QLabel, QListWidgetItem, QMessageBox)
from PyQt6.QtCore import Qt


class ProjectSelectorDialog(QDialog):
    def __init__(self, parent=None, projects_list: list = None):
        super().__init__(parent)
        self.projects = projects_list if projects_list is not None else []
        self.selected_project = None
        
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Select Project")
        self.resize(500, 400)
        
        layout = QVBoxLayout()
        
        title = QLabel("Available Projects:")
        title.setStyleSheet("font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(title)
        
        self.projects_list = QListWidget()
        self.projects_list.itemDoubleClicked.connect(self.accept_selection)
        
        for project in self.projects:
            item = QListWidgetItem(project.name)
            item.setData(Qt.ItemDataRole.UserRole, project.abs_path)
            self.projects_list.addItem(item)
        
        layout.addWidget(self.projects_list)
        
        buttons_layout = QHBoxLayout()
        
        select_btn = QPushButton("Select")
        select_btn.clicked.connect(self.accept_selection)
        buttons_layout.addWidget(select_btn)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        buttons_layout.addWidget(cancel_btn)
        
        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def accept_selection(self):
        """Обрабатывает выбор проекта"""
        current_item = self.projects_list.currentItem()
        if current_item:
            self.selected_project = current_item.data(Qt.ItemDataRole.UserRole)
            self.accept()
        else:
            QMessageBox.warning(self, "Warning", "Please select a project from the list.")

    def get_selected_project(self):
        """Возвращает путь к выбранному проекту"""
        return self.selected_project