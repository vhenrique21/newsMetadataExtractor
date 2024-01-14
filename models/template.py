from typing import Any


class AuthorTemplateModel:
    def __init__(self, **kwargs: Any):
        self.class_names: list[str] = kwargs.get("classNames", [])  # type: ignore
        self.delimiters: list[str] = kwargs.get("delimiters", [])  # type: ignore
        self.prefixes: list[str] = kwargs.get("prefixes", [])  # type: ignore

    class_names: list[str]
    delimiters: list[str]
    prefixes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "class_names": self.class_names,
            "delimiters": self.delimiters,
            "prefixes": self.prefixes,
        }


class CopyrightTemplateModel:
    def __init__(self, **kwargs: Any):
        self.class_names: list[str] = kwargs.get("classNames", [])  # type: ignore
        self.prefixes: list[str] = kwargs.get("prefixes", [])  # type: ignore
        self.sufixes: list[str] = kwargs.get("sufixes", [])  # type: ignore

    class_names: list[str]
    prefixes: list[str]
    sufixes: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "class_names": self.class_names,
            "prefixes": self.prefixes,
            "sufixes": self.sufixes,
        }


class DatetimeTemplateModel:
    def __init__(self, **kwargs: Any):
        self.class_names: list[str] = kwargs.get("classNames", [])  # type: ignore
        self.delimiters: list[str] = kwargs.get("delimiters", [])  # type: ignore
        self.prefixes: list[str] = kwargs.get("prefixes", [])  # type: ignore
        self.dayFirst: bool = kwargs.get("dayFirst", False)  # type: ignore

    class_names: list[str]
    delimiters: list[str]
    prefixes: list[str]
    dayFirst: bool

    def to_dict(self) -> dict[str, Any]:
        return {
            "classNames": self.class_names,
            "delimiters": self.delimiters,
            "prefixes": self.prefixes,
            "dayFirst": self.dayFirst,
        }


class LanguageTemplateModel:
    def __init__(self, **kwargs: Any):
        self.code: str = kwargs.get("code", "")  # type: ignore
        self.complete_code: str = kwargs.get("complete_code", "")  # type: ignore

    code: str
    complete_code: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "code": self.code,
            "complete_code": self.complete_code,
        }


class TemplateModel:
    def __init__(self, **kwargs: Any):
        self.author: AuthorTemplateModel = AuthorTemplateModel(**kwargs["author"])
        self.datetime: DatetimeTemplateModel = DatetimeTemplateModel(
            **kwargs["datetime"]
        )
        self.copyright: CopyrightTemplateModel = CopyrightTemplateModel(
            **kwargs["copyright"]
        )
        self.language: LanguageTemplateModel = LanguageTemplateModel(
            **kwargs["language"]
        )

    author: AuthorTemplateModel
    copyright: CopyrightTemplateModel
    datetime: DatetimeTemplateModel
    language: LanguageTemplateModel

    def to_dict(self) -> dict[str, Any]:
        return {
            "author": self.author.to_dict(),
            "datetime": self.datetime.to_dict(),
            "copyright": self.copyright.to_dict(),
            "language": self.language.to_dict(),
        }
