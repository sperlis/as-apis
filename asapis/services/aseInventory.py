from asapis.services.baseServiceLib import BaseServiceLib
from asapis.services.baseServiceLib import BaseServiceLib

class NotFoundInventoryError(Exception):
    pass

class ASEInventory:
    
    applications = {}
    folders = {}
    templates = {}
    test_policies = {}

    def load(self, ase:BaseServiceLib):
        self.applications = ase.get("applications").json()
        self.folders = ase.get("folders").json()
        self.templates = ase.get("templates").json()
        self.test_policies = ase.get("testpolicies").json()

    # Search for an application with the given name
    # if name is not found, maybe the name IS the ID, so we return it
    def get_application_id(self, name:str) -> int:
        return self.__get_generic_id(name, self.applications, "Application")

    def get_template_id(self, name:str) -> int:
        return self.__get_generic_id(name, self.templates, "Template")

    def get_test_policy_id(self, name:str) -> int:
        return self.__get_generic_id(name, self.test_policies, "Test Policy")

    def get_folder_id(self, path:str) -> int:
        for folder in self.folders:
            if folder["folderPath"] == path:
                return int(folder["folderId"])
        for folder in self.folders:
            if folder["folderPathId"].rstrip('/') == path.rstrip('/'):
                return int(folder["folderId"])
        raise NotFoundInventoryError(f"Folder path '{path}' was not found or not translated to a Path ID")

    def __get_generic_id(self, name:str, source:dict, type:str) -> int:
        for item in source:
            if item["name"] == name:
                return int(item["id"])
        for item in source:
            if item["id"] == name:
                return int(name)
        raise NotFoundInventoryError(f"{type} '{name}' was not found or not translated to an ID")

  