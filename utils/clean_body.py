from copy import deepcopy

from bs4 import Tag

from modules import Parser


def clean_html(parser: Parser) -> None:
    _clean_script(parser)
    _clean_empty_tags(parser)
    _clean_links(parser)


def clean_body(parser: Parser) -> Tag:
    newParser: Tag | Parser = deepcopy(parser.body) or Parser(parser.html)

    for data in newParser.find_all(
        [
            "script",
            "style",
            "iframe",
            "noscript",
            "meta",
            "svg",
            "img",
            "button",
            "form",
            "input",
            "select",
            "label",
            "figure",
        ]
    ):
        data.decompose()

    _clean_empty_tags(newParser)

    if newParser.header:
        for data in newParser.find_all(
            [
                "li",
            ]
        ):
            data.decompose()

    for a in newParser.find_all("a"):
        a.replace_with(a.text)

    _clean_links(newParser)

    for div in newParser.find_all("div"):
        contents: list[str] = div.find_all(text=True, recursive=False)
        if len(contents) and contents[0].strip() != "":
            new_tag = parser.new_tag("b")  # pyright: ignore [reportUnknownMemberType]
            new_tag.string = div.text.strip()
            div.replace_with(new_tag)
        else:
            div.parent.div.unwrap()

    with open("test.html", "w", encoding="utf-8") as file:
        file.write(newParser.prettify())

    return newParser


def _clean_empty_tags(parser: Parser | Tag) -> None:
    for data in parser.find_all():
        if not data.text.strip() and data.name not in ["br", "img"]:
            data.decompose()


def _clean_links(parser: Parser | Tag) -> None:
    for a in parser.find_all("a"):
        a.replace_with(a.text)


def _clean_script(parser: Parser | Tag):
    for data in parser.find_all(["script", "style"]):
        data.decompose()
