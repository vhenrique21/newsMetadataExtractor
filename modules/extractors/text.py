from bs4 import NavigableString, Tag

from models.tag_content import TagContent
from models.template import TemplateModel
from modules.extractors.base import BaseExtractor
from modules.parser import Parser
from utils import clean_body


class TextExtractor(BaseExtractor):
    def __init__(self, parser: Parser, template: TemplateModel):
        super().__init__(parser, template)

    def _extract(self) -> str:
        article: Tag | NavigableString = self._get_article_text()

        if type(article) is Tag:
            extracted_text = article.find_all(text=True, recursive=True)
            text: str = str.join("", [str(x) for x in extracted_text])
            return " ".join(text.split())

        return str(article)

    def _get_article_text(self) -> Tag | NavigableString:
        body: Tag = clean_body(self._parser)
        main = body.find("main")
        article = main.find("article") if type(main) is Tag else None

        return article or main or body

    def extract(self) -> list[TagContent]:
        text: str = self._extract()

        return [
            TagContent(
                name="text",
                value=text,
            )
        ]
