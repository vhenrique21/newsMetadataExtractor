from typing import Any


def flatten(list_of_lists: list[list[Any]]) -> list[Any]:
    return [item.strip() for sublist in list_of_lists for item in sublist]
