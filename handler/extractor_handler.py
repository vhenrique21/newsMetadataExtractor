import itertools

from handler.base import BaseHandler
from models.tag_content import TagContent
from models.template import TemplateModel
from modules.download import NewsDownloader
from modules.extractors.base import BaseExtractor
from modules.extractors.metadata import (
    AuthorsExtractor,
    DatetimeExtractor,
    SubtitleExtractor,
    TitleExtractor,
)
from modules.extractors.metadata.copyright import CopyrightExtractor
from modules.extractors.metadata.keywords import KeywordsExtractor
from modules.extractors.metadata.site_name import SiteNameExtractor
from modules.extractors.metadata.url import UrlExtractor
from modules.extractors.text import TextExtractor
from modules.parser import Parser


class ExtractorHandler(BaseHandler[list[TagContent]]):
    def __init__(self, url: str, template: TemplateModel):
        self._template: TemplateModel = template
        self._parser: Parser = self._downloadNews(url)
        super().__init__(url)

    def _extract(self, extractor: BaseExtractor) -> list[TagContent]:
        tags: list[TagContent] = extractor.extract()
        return tags

    def _downloadNews(self, url: str) -> Parser:
        html: str = NewsDownloader().download(url)
        parser: Parser = Parser(html).parse()
        return parser

    def handle(self):
        title = TitleExtractor(self._parser, self._template).extract()
        subtitle = SubtitleExtractor(self._parser, self._template, title[0]).extract()

        authors = AuthorsExtractor(
            self._parser, self._template, title[0], subtitle[0]
        ).extract()
        datetime = DatetimeExtractor(
            self._parser, self._template, title[0], subtitle[0]
        ).extract()

        url = UrlExtractor(self._parser, self._template).extract()
        copyright = CopyrightExtractor(self._parser, self._template).extract()
        site_name = SiteNameExtractor(
            self._parser, self._template, copyright[0]
        ).extract()

        text: list[TagContent] = TextExtractor(self._parser, self._template).extract()
        keywords = KeywordsExtractor(
            self._parser, self._template, title[0], subtitle[0], text[0]
        ).extract()

        print(text)

        a = [title, subtitle, authors, datetime, url, site_name, keywords]
        flattened_list = list(itertools.chain.from_iterable(a))
        print(flattened_list)
        return flattened_list
