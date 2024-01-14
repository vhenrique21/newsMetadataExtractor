def is_null_or_empty(value: str | list[str] | None) -> bool:
    if type(value) is str:
        return len(value.strip()) == 0

    if type(value) is list[str | None]:
        return len([x for x in value if (x.strip() != "")]) == 0

    return True
