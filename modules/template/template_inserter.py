import json

from models.template import TemplateModel
from utils import generate_hash


class TemplateInserter:
    def __init__(self):
        pass

    def insert(self, url: str, template: TemplateModel):
        file_name = self._save_json(url, template)
        self._add_to_dictionary(url, file_name)

    def _save_json(self, url: str, template: TemplateModel):
        file_name = generate_hash(url)
        file_path = f"./data/templates/{file_name}.json"

        template_dict = template.to_dict()
        with open(file_path, "w") as file:
            json.dump(template_dict, file)

        return file_name

    def _add_to_dictionary(self, url: str, template_name: str):
        template_dictionary: dict[str, str] = json.load(
            open("./data/template_dictionary.json")
        )

        template_dictionary[url] = template_name

        with open("./data/template_dictionary.json", "w") as file:
            json.dump(template_dictionary, file)
