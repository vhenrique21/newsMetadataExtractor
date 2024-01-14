def to_list(value: str | list[str]) -> list[str]:
    if type(value) is list:
        return value
    elif type(value) is str:
        return [value]

    return []
