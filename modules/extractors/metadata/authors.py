from bs4 import ResultSet, Tag

from models import AuthorExtractModel, TagContent, TemplateModel
from modules.extractors import BaseExtractor, MetaTagExtractor
from modules.parser import Parser
from utils import extract_from_extractor, flatten, parse_author


class AuthorsExtractor(BaseExtractor):
    def __init__(
        self,
        parser: Parser,
        template: TemplateModel,
        title: TagContent,
        subtitle: TagContent,
    ):
        self._title: TagContent = title  # type: ignore
        self._subtitle: TagContent = subtitle  # type: ignore
        super().__init__(parser, template)

    def _extract_meta(self) -> str:
        return extract_from_extractor(
            MetaTagExtractor(self._parser, self._template), "author"
        )

    def _extract_by_class(self) -> list[str]:
        tags: ResultSet[Tag] = self._parser.find_all(
            class_=lambda x: x
            and (any(v in x.lower() for v in self._template.author.class_names))
            or False
        )

        values: list[str] = flatten(
            [x.find_all(text=True, recursive=True) for x in tags]
        )

        return [v.strip().replace("\xa0", " ") for v in values if v.strip() != ""]

    def _extract(self) -> AuthorExtractModel:
        return {
            "class_name": parse_author(self._extract_by_class(), self._template),
            "meta": parse_author(self._extract_meta(), self._template),
        }

    def extract(self) -> list[TagContent]:
        data: AuthorExtractModel = self._extract()
        authors: list[str] = _AuthorCombinator(data).combine()
        return [TagContent(name="author", value=authors)] if authors else []


class _AuthorCombinator:
    def __init__(self, data: AuthorExtractModel) -> None:
        self.data: AuthorExtractModel = data

    def _combine(self) -> list[str]:
        combined_set: set[str] = set(self.data["class_name"]) & set(self.data["meta"])
        return list(combined_set) if len(combined_set) else []

    def combine(self) -> list[str]:
        return self._combine() or self.data["meta"] or self.data["class_name"] or [""]
