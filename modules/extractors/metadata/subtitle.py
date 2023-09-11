from bs4 import ResultSet, Tag

from models import SubtitleExtractModel, TagContent
from modules.extractors import BaseExtractor
from modules.extractors.meta import MetaTagExtractor, OpenGraphExtractor
from modules.parser import Parser
from utils import (
    clean_body,
    contains_exact,
    extract_by_tag,
    extract_from_extractor,
    extract_tag_text,
)


class SubtitleExtractor(BaseExtractor):
    def __init__(self, parser: Parser, title: TagContent):
        self._title: TagContent = title  # type: ignore
        super().__init__(parser)

    def _extract_h2(self) -> list[str]:
        return extract_by_tag(self._parser, "h2")

    def _extract_position(self) -> list[str]:
        body: Tag = clean_body(self._parser)
        h1_collection: ResultSet[Tag] = body.find_all("h1", string=self._title["value"])
        h1: Tag | None = h1_collection[0] if len(h1_collection) else None

        if not h1:
            return []

        siblings = h1.find_next_siblings()
        return extract_tag_text(siblings[0]) if len(siblings) else []

    def _extract_meta(self) -> str:
        return extract_from_extractor(MetaTagExtractor(self._parser), "description")

    def _extract_open_graph(self) -> str:
        return extract_from_extractor(OpenGraphExtractor(self._parser), "description")

    def _extract(self) -> SubtitleExtractModel:
        return {
            "position": self._extract_position(),
            "h2": self._extract_h2(),
            "meta": self._extract_meta(),
            "og": self._extract_open_graph(),
        }

    def extract(self) -> list[TagContent]:
        data: SubtitleExtractModel = self._extract()
        subtitle: str = _SubtitleCombinator(data).combine()
        return [TagContent(name="description", value=subtitle)]


class _SubtitleCombinator:
    def __init__(self, data: SubtitleExtractModel) -> None:
        self.data: SubtitleExtractModel = data

    def _combine_h2(self, field: str) -> str | None:
        value: str | None = self.data.get(field)
        return value and contains_exact(value, self.data["h2"])

    def combine(self) -> str:
        subtitle: str | None = (
            self._combine_h2("og")
            or self._combine_h2("meta")
            or self._combine_h2("position")
        )

        if subtitle:
            return subtitle

        if contains_exact(self.data["og"], self.data["position"]):
            return self.data["og"]

        if self.data["meta"] and contains_exact(
            self.data["meta"], self.data["position"]
        ):
            return self.data["meta"]

        if self.data["og"]:
            return self.data["og"]

        if self.data["meta"]:
            return self.data["meta"]

        return ""
