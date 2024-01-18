from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class BaseGenerator(ABC, Generic[T]):
    def __init__(self, **kwargs: dict[str, Any]):
        self._kwargs: dict[str, Any] = kwargs

    @abstractmethod
    def generate(self) -> T:
        pass
