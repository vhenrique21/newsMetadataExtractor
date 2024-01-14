import json

from handler.base import BaseHandler
from models.template import TemplateModel
from modules.template.template_inserter import TemplateInserter
from modules.template.template_selector import TemplateSelector


class TemplateHandler(BaseHandler[TemplateModel]):
    def __init__(self, url: str, template_string: str | None):
        self.templateInservter = TemplateInserter()
        self.TemplateSelector = TemplateSelector()
        self._template_string = template_string
        super().__init__(url)

    def _parse_template(self) -> TemplateModel | None:
        try:
            if self._template_string is None:
                return None

            json_content = json.loads(self._template_string)
            return TemplateModel(**json_content)
        except:
            pass

    def handle(self) -> TemplateModel:
        template: TemplateModel | None = self._parse_template()

        if template:
            self.templateInservter.insert(self._url, template)
            return template

        return self.TemplateSelector.select(self._url)
