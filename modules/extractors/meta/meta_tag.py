from models import TemplateModel
from modules.extractors import BaseExtractor, TagContent
from modules.parser import Parser


class MetaTagExtractor(BaseExtractor):
    target_field: str = "name"
    attrs: dict[str, bool] = {target_field: True}

    def __init__(self, parser: Parser, template: TemplateModel):
        super().__init__(parser, template)

    def _extract_tags(self, results: list[dict[str, str]]) -> list[TagContent]:
        return [
            TagContent(name=tag[self.target_field], value=tag["content"])
            for tag in results
        ]

    def extract(self) -> list[TagContent]:
        result_set = self._parser.find_all("meta", attrs=self.attrs)
        tags: list[dict[str, str]] = self._get_tags(result_set)
        return self._extract_tags(tags)
