from bs4 import ResultSet, Tag

from models.tag_content import TagContent
from modules.extractors.base import BaseExtractor
from modules.parser import Parser
from utils import contains, flatten

content_list = [
    "all rights reserved",
    "todos os direitos reservados",
    "copyright",
    "©",
]
class_list: list[str] = ["copyright"]


class CopyrightExtractor(BaseExtractor):
    def __init__(self, parser: Parser):
        super().__init__(parser)

    def _extract_by_content(self):
        tags: ResultSet[Tag] = self._parser.find_all(
            text=lambda x: x and (any(v in x.lower() for v in content_list)) or False,
            recursive=True,
        )

        values = [t.text for t in tags if t.text.strip() != ""]
        return list(dict.fromkeys(values))

    def _extract_by_class(self) -> list[str]:
        tags: ResultSet[Tag] = self._parser.find_all(
            class_=lambda x: x and (any(v in x.lower() for v in class_list)) or False,
            recursive=True,
        )

        extra_tags = self._parser.find_all(
            attrs={"data-testid": "copyright"},
        )

        tags.extend(extra_tags)

        values: list[str] = flatten(
            [x.find_all(text=True, recursive=True) for x in tags]
        )

        values.extend([x.text for x in tags])

        fitered_values = [
            v.strip().replace("\xa0", " ") for v in values if v.strip() != ""
        ]
        return list(dict.fromkeys(fitered_values))

    def _extract(self):
        by_class = self._extract_by_class()
        by_content = self._extract_by_content()
        return flatten([by_class, by_content])

    def extract(self) -> list[TagContent]:
        data = self._extract()
        copyright = CopyrightCombinator(data).combine()
        return [TagContent(name="copyright", value=copyright)]


class CopyrightCombinator:
    def __init__(self, data: list[str]):
        self.data: list[str] = data

    def _combine(self, data: list[str]) -> str:
        for value in data:
            new_list = [x for x in data if x != value]
            if contains(value, new_list):
                return value

        return data[0]

    def combine(self) -> str:
        data = sorted(self.data, key=len, reverse=True)

        if len(data):
            for i in content_list:
                res = list(filter(lambda x: i in x.lower(), data))
                if res:
                    return self._combine(res)

            return data[0]

        return ""
