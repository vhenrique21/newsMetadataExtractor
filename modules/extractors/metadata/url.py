from models import TagContent, TemplateModel
from modules.extractors.base import BaseExtractor
from modules.parser import Parser
from utils import get_url


class UrlExtractor(BaseExtractor):
    def __init__(self, parser: Parser, template: TemplateModel):
        super().__init__(parser, template)

    def extract(self) -> list[TagContent]:
        data = get_url(self._parser)
        return [TagContent(name="url", value=data)]
