import logging
import pathlib

from ... import context
from .. import date
from .. import structures as base_struct
from ..formatter import Formatter as BaseFormatter
from .structures import LogPlain


class Formatter(BaseFormatter):
    """Plain Formatter."""

    def format(self, record: logging.LogRecord) -> str:
        log = LogPlain(
            date=self.formatTime(record, datefmt=date.FORMAT),
            context=base_struct.LogContext(
                path=pathlib.Path(record.pathname).name,
                line=record.lineno,
            ),
            level=record.levelname,
            message=record.getMessage(),
            request_id=getattr(record, context.ctx_request_id.name, None),
            traceback=self._get_trace(record),
            extra=getattr(record, "extra", None),
        )

        return str(log)
