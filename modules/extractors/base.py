from abc import ABC, abstractmethod
from typing import Any

from bs4 import ResultSet

from models.tag_content import TagContent
from models.template import TemplateModel
from modules.parser import Parser


class BaseExtractor(ABC):
    def __init__(
        self, parser: Parser, template: TemplateModel, **kwargs: dict[str, Any]
    ):
        self._parser: Parser = parser
        self._template: TemplateModel = template
        self._kwargs: dict[str, Any] = kwargs

    def _get_tags(self, results: ResultSet[Any]) -> list[dict[str, str]]:
        return [result.attrs for result in results]

    @abstractmethod
    def extract(self) -> list[TagContent]:
        pass

    def get_html(self) -> str:
        return self._parser.prettify()
