from models import TagContent
from modules.extractors.base import BaseExtractor
from modules.extractors.meta.meta_tag import MetaTagExtractor
from modules.parser import Parser
from utils import extract_from_extractor


class KeywordsExtractor(BaseExtractor):
    def __init__(self, parser: Parser):
        super().__init__(parser)

    def _extract_meta(self) -> list[str]:
        return extract_from_extractor(MetaTagExtractor(self._parser), "keywords").split(
            ","
        )

    def extract(self) -> list[TagContent]:
        data = self._extract_meta()
        return [TagContent(name="keywords", value=data)] if data else []
