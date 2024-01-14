from typing import Literal, Union

from models import TagContent
from modules.extractors import BaseExtractor
from utils import flatten
from utils.is_null_or_empty import is_null_or_empty
from utils.to_list import to_list

TargetMetaTags = Literal[
    "title",
    "description",
    "author",
    "keywords",
    "image",
    "publish_date",
    "publication_date",
    "url",
]

TargetOpenGraphTags = Literal[
    "title",
    "description",
    "url",
    "type",
    "image",
    "locale",
    "site_name",
    "published_time",
]

TargetTags = Union[TargetMetaTags, TargetOpenGraphTags]


def extract_from_extractor(
    extractor: BaseExtractor, target_tag: TargetTags | list[TargetTags]
) -> str:
    if type(target_tag) == str:
        target_tag = [target_tag]

    tags: list[TagContent] = extractor.extract()

    filtered_tags: list[TagContent] = [
        tag
        for tag in tags
        if ((tag["name"] in target_tag) and (is_null_or_empty(tag["value"]) is False))
    ]

    collection: list[list[str]] = [to_list(tag["value"]) for tag in filtered_tags]
    items: list[str] = flatten(collection)

    return ", ".join(items)
