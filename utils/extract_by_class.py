from bs4 import ResultSet, Tag

from modules.parser import Parser
from utils.flatten import flatten


def extract_by_class(parser: Parser, class_list: list[str]) -> list[str]:
    tags: ResultSet[Tag] = parser.find_all(
        class_=lambda x: (x and any(v in x.lower() for v in class_list)) or False
    )

    values: list[str] = flatten([x.find_all(text=True, recursive=True) for x in tags])

    return [v.strip().replace("\xa0", " ") for v in values if v.strip() != ""]
