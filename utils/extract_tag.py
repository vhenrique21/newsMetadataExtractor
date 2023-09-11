from bs4 import BeautifulSoup, PageElement, Tag

from utils.flatten import flatten


def extract_by_tag(parser: BeautifulSoup, tag: str) -> list[str]:
    output_collection: list[list[str]] = [
        t.find_all(string=True) for t in parser.find_all(tag)
    ]

    output: list[str] = flatten(output_collection)

    return [value for value in output if value.strip() != ""]


def extract_tag_text(tag: Tag | PageElement) -> list[str]:
    if type(tag) == Tag:
        contents = tag.find_all(text=True, recursive=True)
        return [c.strip() for c in contents if c.strip() != ""]

    return [tag.get_text().strip().replace("\xa0", " ")]
