from typing import TypedDict


class TagContent(TypedDict):
    name: str
    value: str | list[str]
