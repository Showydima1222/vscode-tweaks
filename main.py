import json
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QMenuBar, 
                             QMessageBox, QInputDialog, QFileDialog, QDialog,
                             QVBoxLayout, QScrollArea, QCheckBox, QLabel, QFrame, QHBoxLayout)
from PyQt6.QtGui import QAction, QScreen

from projects import ProjectHandler, Project
from app.projects_window import ProjectSelectorDialog
from tweaks import TWEAKS, Tweak, find_tweak_by_id
import os
import sys

APP_NAME = "VSCode Tweaks"

class TweakManager:
    def __init__(self, main_window):
        self.main_window = main_window
        self.tweaks_widget = None
        self.tweak_checkboxes = {}
        self.tweak_widgets = {}

    def create_tweaks_interface(self, tweaks_list):
        """Creates ui of tweaks list"""
        container = QWidget()
        layout = QVBoxLayout(container)
        
        title = QLabel("Available Tweaks")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")
        layout.addWidget(title)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        tweaks_content = QWidget()
        tweaks_layout = QVBoxLayout(tweaks_content)
        tweaks_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        for tweak in tweaks_list:
            tweak_widget = self.create_tweak_widget(tweak)
            tweaks_layout.addWidget(tweak_widget)
            self.tweak_widgets[tweak.id] = tweak_widget
        
        scroll_area.setWidget(tweaks_content)
        layout.addWidget(scroll_area)
        
        self.tweaks_widget = container
        self.tweaks_widget.hide()
        return container

    def create_tweak_widget(self, tweak):
        """Creates tweak view"""
        frame = QFrame()
        frame.setFrameStyle(QFrame.Shape.Box)
        frame.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
            }
            QFrame:hover {
                background-color: #e9ecef;
            }
        """)
        
        layout = QVBoxLayout(frame)
        
        header_layout = QHBoxLayout()
        
        checkbox = QCheckBox(tweak.name)
        checkbox.toggled.connect(lambda checked, t_id=tweak.id: self.on_tweak_toggled(t_id, checked))
        checkbox.setToolTip(tweak.description)
        
        self.tweak_checkboxes[tweak.id] = checkbox
        header_layout.addWidget(checkbox)
        
        if tweak.has_conflicts:
            conflict_label = QLabel("⚠️ Conflicts")
            conflict_label.setStyleSheet("color: #dc3545; font-size: 10px;")
            conflict_label.setToolTip(f"Conflicts with: {', '.join(tweak.conflicts)}")
            header_layout.addWidget(conflict_label)
            header_layout.addStretch()
        
        
        if tweak.description:
            description = QLabel(tweak.description)
            description.setWordWrap(True)
            description.setStyleSheet("color: #6c757d; font-size: 11px; margin-left: 20px;")
            layout.addWidget(description)
        
        return frame

    def on_tweak_toggled(self, tweak_id, checked):
        """When tweak selection changed"""
        self.main_window.handle_tweak_toggle(tweak_id, checked)

    def show_tweaks_interface(self):
        """Shows tweaks ui (when project selected)"""
        if self.tweaks_widget:
            self.tweaks_widget.show()

    def hide_tweaks_interface(self):
        """Hides tweaks ui (when project is closed)"""
        if self.tweaks_widget:
            self.tweaks_widget.hide()

    def get_selected_tweaks(self):
        """Returns selected tweaks ids"""
        return [tweak_id for tweak_id, checkbox in self.tweak_checkboxes.items() if checkbox.isChecked()]

    def set_selected_tweaks(self, tweak_ids):
        """Restores tweaks from list of tweaks"""
        for checkbox in self.tweak_checkboxes.values():
            checkbox.blockSignals(True)
            checkbox.setChecked(False)
        
        for tweak_id in tweak_ids:
            if tweak_id in self.tweak_checkboxes:
                self.tweak_checkboxes[tweak_id].setChecked(True)
        
        for checkbox in self.tweak_checkboxes.values():
            checkbox.blockSignals(False)

    def clear_selection(self):
        """Resets all selections"""
        for checkbox in self.tweak_checkboxes.values():
            checkbox.setChecked(False)


class MainWindow(QMainWindow):
    def __init__(self, project_handler: ProjectHandler) -> None:
        super().__init__()
        self.project_handler = project_handler
        self.working_project: Project | None = None
        self.tweak_manager = TweakManager(self)
        
        self.setup_ui()
        self.create_menu_bar()

    def setup_ui(self):
        self.setWindowTitle(APP_NAME)
        self.setGeometry(*self.calculate_window_size())
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.main_layout = QVBoxLayout(self.central_widget)
        
        self.welcome_label = QLabel("Welcome to VSCode Tweaks Manager!\nCreate a new project or open an existing one.")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 14px; color: #6c757d; margin: 50px;")
        self.main_layout.addWidget(self.welcome_label)
        
        tweaks_interface = self.tweak_manager.create_tweaks_interface(self.get_available_tweaks())
        self.main_layout.addWidget(tweaks_interface)
        
        self.statusBar().showMessage("Ready")

    def calculate_window_size(self):
        screen = self.screen()
        
        if screen:
            screen_size = screen.availableGeometry()
            screen_width = screen_size.width()
            screen_height = screen_size.height()
            
            window_width = screen_width // 4
            window_height = screen_height // 3
            
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            return x, y, window_width, window_height
        else:
            return 100, 100, 800, 600

    def get_available_tweaks(self):
        return TWEAKS

    def get_enabled_tweaks_from_project(self, project_data):
        return project_data.get("tweaks", [])

    def handle_tweak_toggle(self, tweak_id, checked):
        if self.working_project:
            if checked and tweak_id not in self.working_project.tweaks:
                self.working_project.tweaks.append(tweak_id)
            elif not checked and tweak_id in self.working_project.tweaks:
                self.working_project.tweaks.remove(tweak_id)

    def create_menu_bar(self):
        menubar = self.menuBar()
        
        project_menu = menubar.addMenu("Project")
        
        # New Project
        new_action = QAction("New", self)
        new_action.setStatusTip("Create new project")
        new_action.triggered.connect(self.new_project)
        project_menu.addAction(new_action)
        
        project_menu.addSeparator()
        
        # Open actions
        open_via_manager = QAction("Open via manager", self)
        open_via_manager.setStatusTip("Open project using project manager")
        open_via_manager.triggered.connect(self.open_project)
        project_menu.addAction(open_via_manager)

        open_from_file = QAction("Open from file", self)
        open_from_file.setStatusTip("Open project from JSON file")
        open_from_file.triggered.connect(self.open_project_from_file)
        project_menu.addAction(open_from_file)
        
        project_menu.addSeparator()
        
        # Save actions
        save_action = QAction("Save", self)
        save_action.setStatusTip("Save project changes")
        save_action.triggered.connect(self.save_project)
        project_menu.addAction(save_action)

        save_as_action = QAction("Save as", self)
        save_as_action.setStatusTip("Save project to new file")
        save_as_action.triggered.connect(self.save_project_as)
        project_menu.addAction(save_as_action)
        
        project_menu.addSeparator()
        
        # Apply actions
        save_to_css = QAction("Save to .css", self)
        save_to_css.setStatusTip("Export tweaks to CSS file")
        save_to_css.triggered.connect(self.render_to_css)
        project_menu.addAction(save_to_css)


        if sys.platform == "win32":
            apply_to_vsc = QAction("Apply to VSCode", self)
            apply_to_vsc.setStatusTip("Apply styles to VSCode settings")
            apply_to_vsc.triggered.connect(self.change_path_of_style_to_current)
            project_menu.addAction(apply_to_vsc)


    def change_path_of_style_to_current(self):
        self.render_to_css()
        settings_json = f"{os.getenv('APPDATA')}\\Code\\User\\settings.json"
        if os.path.isfile(settings_json) and self.working_project:
            tag = "custom-ui-style.external.imports"
            settings = {}
            print(settings_json)
            css = "file://"+self.get_css_path(self.working_project.abs_path)
            with open(settings_json, "r") as f:
                l = []
                for line in f.read().split("\n"):
                    a = line.split()
                    if "//" not in a:
                        l.append(line)
                settings = json.loads("\n".join(l))
            settings.update({tag:[css]})
            with open(settings_json, "w") as f:
                json.dump(settings, f)

    def new_project(self):
        name, ok = QInputDialog.getText(
            self, 
            "New Project", 
            "Enter project name:", 
            text=f"project-{len(self.project_handler.projects)}"
        )
        
        if ok and name:
            self.project_handler.new_project(name)
            new_project = self.project_handler.projects[-1]
            self.load_project_from_file(new_project.abs_path)

    def open_project(self):
        dialog = ProjectSelectorDialog(self, self.project_handler.projects)
        
        if dialog.exec() == QDialog.DialogCode.Accepted:
            project_path = dialog.get_selected_project()
            if project_path:
                self.load_project_from_file(project_path)

    def get_css_path(self, original:str) -> str:
        return ".".join(original.split(".")[:-1])+".css"

    def render_to_css(self):
        if self.working_project:
            with open(self.get_css_path(self.working_project.abs_path), "w+") as f:
                f.write("\n".join([find_tweak_by_id(tw).content for tw in self.working_project.tweaks]))

    def open_project_from_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, 
            caption="Open Project", 
            directory=self.project_handler.styles_folder_name, 
            filter="JSON Files (*.json)"
        )
        
        if path:
            self.load_project_from_file(path)

    def load_project_from_file(self, path):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.working_project = Project().from_json(data, path)
                
            self.setWindowTitle(f"{APP_NAME} - {self.working_project.name}")
            self.statusBar().showMessage(f"Project loaded: {self.working_project.name}")
            
            self.welcome_label.hide()
            self.tweak_manager.show_tweaks_interface()
            
            enabled_tweaks = self.get_enabled_tweaks_from_project(data)
            self.tweak_manager.set_selected_tweaks(enabled_tweaks)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load project: {str(e)}")

    def save_project(self):
        if not self.working_project:
            QMessageBox.warning(self, "Warning", "No project is currently open.")
            return
        
        try:
            project_data = {
                "name": self.working_project.name,
                "tweaks": self.tweak_manager.get_selected_tweaks()
            }
            
            with open(self.working_project.abs_path, "w", encoding="utf-8") as f:
                json.dump(project_data, f, indent=4)
                
            self.statusBar().showMessage("Project saved successfully.")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")

    def save_project_as(self):
        if not self.working_project:
            QMessageBox.warning(self, "Warning", "No project is currently open.")
            return
        
        name, ok = QInputDialog.getText(
            self, 
            "Save Project As", 
            "Enter new project name:",
            text=self.working_project.name
        )
        
        if ok and name:
            try:
                enabled_tweaks = self.tweak_manager.get_selected_tweaks()
                self.project_handler.new_project(name, enabled_tweaks)
                
                new_project = self.project_handler.projects[-1]
                self.load_project_from_file(new_project.abs_path)
                
                self.statusBar().showMessage(f"Project saved as: {name}")
                
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")


if __name__ == "__main__":
    app = QApplication([])
    project_handler = ProjectHandler()
    main_window = MainWindow(project_handler)
    main_window.show()
    app.exec()