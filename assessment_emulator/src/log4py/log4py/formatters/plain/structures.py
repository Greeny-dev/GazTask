from dataclasses import dataclass, fields, replace
from typing import Iterable, TypeVar

from ...constants import LogVerbosity
from ...environment import LOG_VERBOSITY
from ...extra_templates import TemplateTypes
from .. import structures as base_struct


@dataclass(slots=True)
class LogPlain(base_struct.Log):
    __MAX_MESSAGE_LEN = 512
    __MAX_EXTRA_FIELD_LEN = 1024
    __TRUNCATION_MARK = "..."

    def __str__(self) -> str:
        message = self.__truncate(self.message, self.__MAX_MESSAGE_LEN)
        traceback = f"\n{self.traceback}" if self.traceback is not None else ""

        if LOG_VERBOSITY is LogVerbosity.LOW:
            return f'[{self.date}] [{self.level:<8s}] "{message}" {traceback}'

        max_file_len = 24
        max_code_no_len = 4
        context = f"{self.context.path[:max_file_len]}:{self.context.line}"
        extra = "" if self.extra is None else self.__truncate_extra(self.extra)
        return (
            f"[{self.date}] "
            f"[{context:<{max_file_len + max_code_no_len}s}] "
            f"[{self.level:<8s}] "
            f'[{self.request_id or "":<36s}] '
            f'"{message}" {extra}'
            f"{traceback}"
        )

    def __truncate_extra(self, extra: TemplateTypes) -> TemplateTypes:
        truncated_instance = replace(extra)  # shallow copy
        types_to_truncate = (str, bytes)
        for field in fields(extra):
            field_value = getattr(extra, field.name)
            if not isinstance(field_value, types_to_truncate):
                continue
            truncated_value = self.__truncate(field_value, self.__MAX_EXTRA_FIELD_LEN)
            setattr(truncated_instance, field.name, truncated_value)
        return truncated_instance

    T = TypeVar("T", bound=Iterable)

    def __truncate(self, value: T, length: int) -> T:
        if len(value) <= length:
            return value
        return value[:length] + self.__TRUNCATION_MARK
