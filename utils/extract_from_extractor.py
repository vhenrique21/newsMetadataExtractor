from typing import Literal, Union

from models import TagContent
from modules.extractors import BaseExtractor

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

DateTargetTags = Union[TargetMetaTags, TargetOpenGraphTags]


def extract_from_extractor(
    extractor: BaseExtractor, target_tag: DateTargetTags | list[DateTargetTags]
) -> str:
    if type(target_tag) == str:
        target_tag = [target_tag]

    tags = extractor.extract()

    title_tags: list[TagContent] = [tag for tag in tags if tag["name"] in target_tag]
    title_tags = [tag for tag in title_tags if tag["value"].strip() != ""]

    return title_tags[0]["value"] if len(title_tags) > 0 else ""
