from typing import Tuple


def contains_exact(l1: str | list[str], l2: list[str]) -> str | None:
    if type(l1) == str:
        l1 = [l1]

    list1_formated, list2_formated = _format(l1, l2)

    for idx, value in enumerate(list1_formated):
        if value in sorted(list2_formated, key=len, reverse=True):
            return l1[idx]

    for idx, value in enumerate(list2_formated):
        if value in sorted(list1_formated, key=len, reverse=True):
            return l2[idx]

    return None


def contains(l1: str | list[str], l2: list[str]) -> str | None:
    list1_formated, list2_formated = _format(l1, l2)

    for idx, value in enumerate(list1_formated):
        if any([value in v for v in sorted(list2_formated, key=len, reverse=True)]):
            return l1[idx]

    for idx, value in enumerate(list2_formated):
        if any([value in v for v in sorted(list1_formated, key=len, reverse=True)]):
            return l2[idx]

    return None


def _format(l1: str | list[str], l2: list[str]) -> Tuple[list[str], list[str]]:
    if type(l1) == str:
        l1 = [l1]

    l1 = [s.strip().lower() for s in l1 if s.strip() != ""]
    l2 = [s.strip().lower() for s in l2 if s.strip() != ""]

    return l1, l2
