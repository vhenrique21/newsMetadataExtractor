from models import TemplateModel
from modules.extractors import BaseExtractor, TagContent
from modules.parser import Parser


class OpenGraphExtractor(BaseExtractor):
    target_field: str = "property"
    attrs: dict[str, bool] = {target_field: True}

    def __init__(self, parser: Parser, template: TemplateModel):
        super().__init__(parser, template)

    def _filter_tags(self, tags: list[dict[str, str]]) -> list[dict[str, str]]:
        return [tag for tag in tags if tag[self.target_field].startswith("og:")]

    def _build_tag_name(self, tag: str) -> str:
        return tag.replace("og:", "")

    def _extract_tags(self, results: list[dict[str, str]]) -> list[TagContent]:
        output: list[TagContent] = []

        for tag in self._filter_tags(results):
            name: str = self._build_tag_name(tag[self.target_field])
            value: str = tag["content"]
            output.append(TagContent(name=name, value=value))

        return output

    def extract(self) -> list[TagContent]:
        result_set = self._parser.find_all("meta", attrs=self.attrs)
        tags: list[dict[str, str]] = self._get_tags(result_set)
        return self._extract_tags(tags)
