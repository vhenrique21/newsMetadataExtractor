from bs4 import Tag

from modules.parser import Parser


def get_url(parser: Parser) -> str:
    head: Tag | None = parser.head
    url = head and head.find("meta", {"name": "url"})
    return url["content"] if url else ""  # type: ignore
