# pyright: reportUnknownMemberType=false
import re
from typing import Self

from bs4 import BeautifulSoup


class Parser(BeautifulSoup):
    def __init__(self, html: str):
        self.html = re.sub(r"<!.*?->", "", html)
        super().__init__(re.sub(r"<!.*?->", "", html), "html.parser")

    def _clean(self):
        for data in self.find_all(["script", "style"]):
            data.decompose()

        for a in self.find_all("a"):
            a.replace_with(a.text)

    def parse(self) -> Self:
        self._clean()
        return self
