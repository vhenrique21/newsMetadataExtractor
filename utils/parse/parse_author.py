import re

from utils import contains
from utils.parse.parse_date import parse_date

SEPARATORS = [" and ", ", ", " & ", " e "]
PREFIXES = ["by", "edited by", "por", "di", "dal"]


def parse_author(input: list[str] | str) -> list[str]:
    if type(input) == str:
        authors: list[str] = _parse_name(input)
        return _remove_duplicates(authors)

    input = list(dict.fromkeys(input))
    input = [i for i in input if not parse_date(i)]

    string_without_prefix: str = _parse_prefix(input)

    authors: list[str] = _parse_name(string_without_prefix)
    return _remove_duplicates(authors)


def _parse_prefix(input: list[str]):
    for idx, text in enumerate(input):
        for prefix in PREFIXES:
            if text.lower().startswith(prefix):
                text = re.sub(r"^" + prefix, "", text, flags=re.IGNORECASE)
                if text.strip() == "":
                    input.pop(idx)
                    return ", ".join(input)
                return text

    return ", ".join(input)


def _parse_name(input: str) -> list[str]:
    regex = "|".join(SEPARATORS)
    authors: list[str] = re.split(regex, input)
    return [a.strip() for a in authors if a.strip() != ""]


def _remove_duplicates(input: list[str]) -> list[str]:
    for idx, author in enumerate(input):
        if contains(author, input[:idx] + input[idx + 1 :]):
            return [author]

    return input


# def _check_for_date(input: str) -> Tuple[bool, datetime | None]:
#     try:
#         parse(input, ignoretz=True)
#         return True, parse(input, ignoretz=True)
#     except ValueError:
#         return False, None
