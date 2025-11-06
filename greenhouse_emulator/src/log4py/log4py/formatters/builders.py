import abc
import logging

from ..constants import LogFormat
from . import json_, plain


class Builder(abc.ABC):
    """Base class for `logging.Formatter` builders."""

    @abc.abstractmethod
    def __call__(self, **kwargs) -> logging.Formatter:
        pass

    @property
    @abc.abstractmethod
    def format(self) -> LogFormat:
        pass

    def __str__(self) -> str:
        return f"{self.__class__}:{self.format}"


class PlainFormatterBuilder(Builder):
    @property
    def format(self) -> LogFormat:
        return LogFormat.PLAIN

    def __call__(self, **_ignored) -> logging.Formatter:
        return plain.Formatter()


class JsonFormatterBuilder(Builder):
    @property
    def format(self) -> LogFormat:
        return LogFormat.JSON

    def __call__(self, **_ignored) -> json_.Formatter:
        return json_.Formatter()
