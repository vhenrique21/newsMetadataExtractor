from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseHandler(ABC, Generic[T]):
    def __init__(self, url: str, **kwargs: dict[str, Any]):
        self._url: str = url
        self._kwargs: dict[str, Any] = kwargs

    @abstractmethod
    def handle(self) -> T:
        pass
