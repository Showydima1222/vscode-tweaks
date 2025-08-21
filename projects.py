import os
import json


class ProjectHandler:
    EMPTY_PROJECT = {"name": "", "tweaks": []}
    
    def __init__(self, styles_folder_name: str = "styles") -> None:
        self.styles_folder_name = styles_folder_name
        self._prepare_dirs()
        self.projects = self.load_projects()

    def _prepare_dirs(self):
        if not os.path.exists(self.styles_folder_name):
            os.makedirs(self.styles_folder_name)

    def load_projects(self) -> list:
        projects = []
        
        if not os.path.exists(self.styles_folder_name):
            return projects
        
        for file in os.listdir(self.styles_folder_name):
            if file.endswith(".json"):
                file_path = os.path.join(self.styles_folder_name, file)
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    if all(key in data for key in self.EMPTY_PROJECT.keys()):
                        projects.append(Project().from_json(data, os.path.abspath(file_path)))
                        
                except Exception as e:
                    print(f"Error loading project {file}: {e}")
        
        return projects
    
    def new_project(self, name: str, tweaks: list = None):
        if tweaks is None:
            tweaks = []
            
        file_path = os.path.join(self.styles_folder_name, f"{name}.json")
        project_data = {
            "name": name,
            "tweaks": tweaks
        }
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(project_data, f, indent=4)
            
            self.projects.append(Project(name, tweaks, os.path.abspath(file_path)))
            
        except Exception as e:
            raise Exception(f"Failed to create project: {e}")


class Project:
    def __init__(self, name: str = "", tweaks: list = None, abs_path: str = "") -> None:
        self.name = name
        self.tweaks = tweaks if tweaks is not None else []
        self.abs_path = abs_path
    
    def from_json(self, data: dict, abs_path: str):
        return Project(
            data.get("name", ""), 
            data.get("tweaks", []), 
            abs_path
        )