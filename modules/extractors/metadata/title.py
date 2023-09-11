from models import TagContent, TitleExtractModel
from modules.extractors import BaseExtractor
from modules.extractors.meta import MetaTagExtractor, OpenGraphExtractor
from modules.parser import Parser
from utils import contains_exact, extract_by_tag, extract_from_extractor, is_substring


class TitleExtractor(BaseExtractor):
    def __init__(self, parser: Parser):
        super().__init__(parser)

    def _extract_title_tag(self) -> str:
        head = self._parser.head
        title = head and head.title
        return str(title.contents[0]) if title else ""

    def _extract_h1(self) -> list[str]:
        return extract_by_tag(self._parser, "h1")

    def _extract_meta(self) -> str:
        return extract_from_extractor(MetaTagExtractor(self._parser), "title")

    def _extract_open_graph(self) -> str:
        return extract_from_extractor(OpenGraphExtractor(self._parser), "title")

    def _extract(self) -> TitleExtractModel:
        return {
            "title": self._extract_title_tag(),
            "h1": self._extract_h1(),
            "meta": self._extract_meta(),
            "og": self._extract_open_graph(),
        }

    def extract(self) -> list[TagContent]:
        data: TitleExtractModel = self._extract()
        title: str = _TitleCombinator(data).combine()
        return [TagContent(name="title", value=title)]


class _TitleCombinator:
    def __init__(self, data: TitleExtractModel) -> None:
        self.data: TitleExtractModel = data

    def _combine_h1(self, field: str) -> str | None:
        value: str | None = self.data.get(field)
        if value and contains_exact(value, self.data["h1"]):
            return value

    def _combine_substring(self) -> str | None:
        for h1 in self.data["h1"]:
            if (
                is_substring(h1, self.data["title"])
                or is_substring(h1, self.data["meta"])
                or is_substring(h1, self.data["og"])
            ):
                return h1

    def combine(self) -> str:
        title: str | None = (
            self._combine_h1("title")
            or self._combine_h1("meta")
            or self._combine_h1("og")
        )

        if title is None:
            title = self._combine_substring()

        return title or self.data["title"]
