from models import TagContent
from models.template import TemplateModel
from modules.extractors.base import BaseExtractor
from modules.extractors.meta.meta_tag import MetaTagExtractor
from modules.generator.KeywordGenerator import KeywordsGenerator
from modules.parser import Parser
from utils import extract_from_extractor


class KeywordsExtractor(BaseExtractor):
    def __init__(
        self,
        parser: Parser,
        template: TemplateModel,
        title: TagContent,
        subtitle: TagContent,
        text: TagContent,
    ):
        self._title: TagContent = title
        self._subtitle: TagContent = subtitle
        self._text: TagContent = text
        super().__init__(parser, template)

    def _merge_text(self, tagContent: TagContent) -> str:
        return (
            tagContent["value"]
            if type(tagContent["value"]) == str
            else " ".join(tagContent["value"])
        )

    def _merge_texts(self) -> str:
        return " ".join(
            [
                self._merge_text(self._title),
                self._merge_text(self._subtitle),
                self._merge_text(self._text),
            ]
        )

    def _extract_meta(self) -> list[str]:
        extracted_meta: list[str] = extract_from_extractor(
            MetaTagExtractor(self._parser, self._template), "keywords"
        ).split(",")

        return [x.strip() for x in extracted_meta if x.strip() != ""]

    def extract(self) -> list[TagContent]:
        data = self._extract_meta()

        if not data:
            text: str = self._merge_texts()

            data: list[str] = KeywordsGenerator(
                text, self._template.language.code
            ).generate()

        return [TagContent(name="keywords", value=data)]
