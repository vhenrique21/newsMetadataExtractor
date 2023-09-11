from dateutil.parser import parse


def parse_date(input: str) -> str | None:
    try:
        input = input.replace("às", "at").replace("Updated", "").strip()
        return str(parse(input, dayfirst=True, ignoretz=True).date())
    except ValueError:
        return None


def parse_dates(input: list[str]) -> list[str]:
    dates: list[str | None] = [parse_date(i) for i in input]
    return sorted([d for d in dates if d])


def filter_string_dates(input: list[str]) -> list[str]:
    return [i for i in input if parse_date(i)]
