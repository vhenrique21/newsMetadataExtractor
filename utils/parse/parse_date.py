from dateutil.parser import parse

from models.template import TemplateModel


def parse_date(input: str, template: TemplateModel) -> str | None:
    try:
        for prefix in template.datetime.prefixes:
            if input.lower().startswith(prefix):
                input = input.replace(prefix, "").strip()

        for delimiter in template.datetime.delimiters:
            if delimiter in input:
                input = input.replace(delimiter, "").strip()

        dayFirst: bool = template.datetime.dayFirst
        date = parse(input, dayfirst=dayFirst, ignoretz=True).date()
        return str(date)

    except ValueError:
        return None


def parse_dates(input: list[str], template: TemplateModel) -> list[str]:
    dates: list[str | None] = [parse_date(i, template) for i in input]
    return sorted([d for d in dates if d])


def filter_string_dates(input: list[str], template: TemplateModel) -> list[str]:
    return [i for i in input if parse_date(i, template)]
