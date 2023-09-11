import hashlib
import os
from typing import Tuple
from urllib.request import Request, urlopen

from modules.parser import Parser


class NewsDownloader:
    path: str = "./downloads/"
    file_extension: str = ".html"

    def __init__(self):
        self._start()

    def _start(self) -> None:
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def _url_hash(self, url: str) -> str:
        return hashlib.sha256(url.encode()).hexdigest()

    def _build_file_path(self, url: str) -> str:
        hash_value = self._url_hash(url)
        return f"{self.path}{hash_value}{self.file_extension}"

    def _try_get_stored_file(self, path: str) -> Tuple[bool, str | None]:
        if not os.path.isfile(path):
            return False, None

        with open(path, "r", encoding="utf-8") as file:
            return True, file.read()

    def download(self, url: str) -> str:
        path = self._build_file_path(url)
        stored, stored_content = self._try_get_stored_file(path)

        if stored:
            return str(stored_content)

        req = Request(
            url=url,
            headers={"User-Agent": "Mozilla/5.0"},
        )

        with urlopen(req) as open_url:
            downloaded_content: str = open_url.read().decode("utf-8")

        downloaded_content = downloaded_content.replace("\t", "").replace("\n", "")

        parser = Parser(downloaded_content)

        metatag = parser.new_tag("meta")  # pyright: ignore [reportUnknownMemberType]
        metatag.attrs["name"] = "url"
        metatag.attrs["content"] = url

        if parser.head:
            parser.head.append(metatag)

        with open(path, "w", encoding="utf-8") as file:
            file.write(str(parser))

        return str(parser)
