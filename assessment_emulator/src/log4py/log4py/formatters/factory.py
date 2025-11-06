import logging

from ..constants import LogFormat
from . import builders
from .errors import NoRealizationFound


class Factory:
    def __init__(self) -> None:
        self._builders: dict[LogFormat, builders.Builder] = dict()

    def get(self, format_: LogFormat, **config) -> logging.Formatter:
        if (builder := self._builders.get(format_)) is None:
            raise NoRealizationFound(format_)
        return builder(**config)

    def register(self, builder: builders.Builder) -> None:
        if (existing_builder := self._builders.get(builder.format)) is not None:
            msg_exc = (
                f"Unable to register more than one builder for same format `{builder.format}`. "
                f"Existing `{existing_builder}` conflicts with `{builder}`"
            )
            raise RuntimeError(msg_exc)
        self._builders[builder.format] = builder


__factory = Factory()

__factory.register(builders.PlainFormatterBuilder())
__factory.register(builders.JsonFormatterBuilder())


def get(format_: LogFormat) -> logging.Formatter:
    """Encapsulate factory registration methods."""
    return __factory.get(format_)
