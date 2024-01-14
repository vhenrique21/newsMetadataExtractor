import json
import os

from models.template import TemplateModel
from utils import extract_url_root


class TemplateSelector:
    def __init__(self):
        self.templates: dict[str, TemplateModel] = self._read_json_files(
            "./data/templates"
        )
        self.template_dictionary: dict[str, str] = self._read_template_dictionary()

    def _read_json_files(self, folder_path: str) -> dict[str, TemplateModel]:
        templates: dict[str, TemplateModel] = {}

        for file_name in os.listdir(folder_path):
            if file_name.endswith(".json"):
                with open(f"{folder_path}/{file_name}") as json_file:
                    try:
                        jsonContent = json.load(json_file)
                        templates[file_name.removesuffix(".json")] = TemplateModel(
                            **jsonContent
                        )
                    except:
                        pass

        return templates

    def _read_template_dictionary(self) -> dict[str, str]:
        return json.load(open("./data/template_dictionary.json"))

    def select(self, url: str) -> TemplateModel:
        template_name: str = (
            self.template_dictionary.get(url)
            or self.template_dictionary.get(extract_url_root(url))
            or self.default()
        )

        return self.templates[template_name]

    def default(self) -> str:
        return self.template_dictionary["default"]
