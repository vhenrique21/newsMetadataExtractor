import re
from difflib import SequenceMatcher

from models.extract_model import SiteNameExtractModel
from models.tag_content import TagContent
from models.template import TemplateModel
from modules.extractors.base import BaseExtractor
from modules.extractors.meta.open_graph_tag import OpenGraphExtractor
from modules.parser import Parser
from utils import extract_from_extractor, get_url


class SiteNameExtractor(BaseExtractor):
    def __init__(self, parser: Parser, template: TemplateModel, copyright: TagContent):
        self.copyright = copyright
        super().__init__(parser, template)

    def _extract_open_graph(self) -> str:
        return extract_from_extractor(
            OpenGraphExtractor(self._parser, self._template), "site_name"
        )

    def _extract_from_regex(self) -> str:
        regex = re.compile(r"^.+?[^\/:](?=[?\/]|$)")

        complete_url = get_url(self._parser).lower()

        regx_match = regex.search(complete_url)
        url = regx_match.group(0) if regx_match else ""

        copyright = str(self.copyright["value"]).lower()

        match = SequenceMatcher(None, url, copyright).find_longest_match()

        return url[match.a : match.a + match.size]

    def _extract(self) -> SiteNameExtractModel:
        return {
            "og": self._extract_open_graph(),
            "regex": self._extract_from_regex(),
        }

    def extract(self) -> list[TagContent]:
        data = self._extract()
        name = SiteNameCombinator(data).extract()
        return [TagContent(name="site_name", value=name)]


class SiteNameCombinator:
    def __init__(self, data: SiteNameExtractModel):
        self.data = data

    def extract(self) -> str:
        return self.data["og"] or self.data["regex"]
