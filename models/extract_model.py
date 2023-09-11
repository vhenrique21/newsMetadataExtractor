from typing import TypedDict


class TitleExtractModel(TypedDict):
    title: str
    h1: list[str]
    meta: str
    og: str


class SubtitleExtractModel(TypedDict):
    position: list[str]
    h2: list[str]
    meta: str
    og: str


class AuthorExtractModel(TypedDict):
    class_name: list[str]
    meta: list[str]


class SiteNameExtractModel(TypedDict):
    regex: str
    og: str


class DatetimeExtractModel(TypedDict):
    class_name: list[str]
    time: list[str]
    url: str | None
    meta: str | None
    og: str | None
