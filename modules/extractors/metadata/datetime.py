import re

from bs4 import Tag

from models import TagContent
from models.extract_model import DatetimeExtractModel
from modules.extractors import BaseExtractor
from modules.extractors.meta import MetaTagExtractor, OpenGraphExtractor
from modules.parser import Parser
from utils import DateTargetTags, extract_by_class, extract_from_extractor, flatten
from utils.parse.parse_date import parse_date, parse_dates

date_target_tags: list[DateTargetTags] = [
    "publication_date",
    "publish_date",
    "published_time",
]


class_list: list[str] = [
    "updated",
    "date",
    "data",
    "time",
    "published-date",
    "timestamp",
    "datetime",
    "date-published",
]


class DatetimeExtractor(BaseExtractor):
    def __init__(self, parser: Parser, title: TagContent, subtitle: TagContent):
        self._title: TagContent = title  # type: ignore
        self._subtitle: TagContent = subtitle  # type: ignore
        super().__init__(parser)

    def _extract_time_tag(self) -> list[str]:
        datetime: list[str] = [
            time["datetime"] if time.get("datetime") else time.text
            for time in self._parser.find_all("time")
        ]
        return datetime

    def _extract_by_class(self) -> list[str]:
        return flatten(
            [d.split("|") for d in extract_by_class(self._parser, class_list)]
        )

    def _extract_from_url(self) -> str:
        head: Tag | None = self._parser.head
        url_tag = head and head.find("meta", {"name": "url"})

        if url_tag:
            url: str = url_tag["content"]  # type: ignore
            regex = re.compile(r"\d{4}[/,-]\d{2}[/,-]\d{2}")
            regex_match = regex.search(url)
            if regex_match:
                return regex_match.group(0)

        return ""

    def _extract_meta(self) -> str:
        return extract_from_extractor(MetaTagExtractor(self._parser), date_target_tags)

    def _extract_open_graph(self) -> str:
        return extract_from_extractor(
            OpenGraphExtractor(self._parser), date_target_tags
        )

    def _extract(self) -> DatetimeExtractModel:
        return {
            "class_name": parse_dates(self._extract_by_class()),
            "time": (lambda x: parse_dates(x) or x)(self._extract_time_tag()),
            "url": parse_date(self._extract_from_url()),
            "meta": parse_date(self._extract_meta()),
            "og": parse_date(self._extract_open_graph()),
        }

    def extract(self) -> list[TagContent]:
        data: DatetimeExtractModel = self._extract()
        date: str = _DatetimeCombinator(data).combine()
        return [TagContent(name="datetime", value=date)]


class _DatetimeCombinator:
    def __init__(self, data: DatetimeExtractModel) -> None:
        self.data: DatetimeExtractModel = data

    def combine(self) -> str:
        if self.data["og"]:
            return self.data["og"]

        if self.data["meta"]:
            return self.data["meta"]

        if self.data["time"]:
            return self.data["time"][0]

        if self.data["class_name"]:
            return self.data["class_name"][0]

        if self.data["url"]:
            return self.data["url"]

        return ""
