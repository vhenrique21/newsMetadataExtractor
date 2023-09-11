import re
from re import Match, Pattern


def equals(string1: str, string2: str):
    string1 = string1.lower().strip()
    string2 = string2.lower().strip()

    pattern: Pattern[str] = re.compile(string2)
    match: Match[str] | None = re.search(pattern, string1)
    return bool(match)
