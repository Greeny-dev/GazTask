import logging
import sys

from . import context
from . import environment as env
from . import extra_templates, filters, formatters


class Logger:
    """
    Wrapper class which encapsulates standard logger.

    Instance of `Logger` class only has methods to log at each standard level of severity:
      - debug (stdout)
      - info (stdout)
      - warning (stderr)
      - error (stderr)
      - critical (stderr)

    Instance of `Logger` class overrides root logger behaviour accordingly at instantiation.
    """

    def __init__(self) -> None:
        self._logger = logging.getLogger(__name__)
        self._logger.propagate = False  # To cancel propagation handlers of root
        self._logger.setLevel(env.LOG_LEVEL)

        self._logger.addFilter(filters.contextual.Filter())
        self._logger.addFilter(filters.framing.Filter(__file__))

        formatter = formatters.get(env.LOG_FORMAT)

        console_out_handler = logging.StreamHandler(sys.stdout)
        console_out_handler.addFilter(lambda record: record.levelno <= logging.INFO)
        console_out_handler.setFormatter(formatter)
        self._logger.addHandler(console_out_handler)

        console_err_handler = logging.StreamHandler(sys.stderr)
        console_err_handler.addFilter(lambda record: record.levelno >= logging.WARNING)
        console_err_handler.setFormatter(formatter)
        self._logger.addHandler(console_err_handler)

        if logging.getLevelName(env.LOG_LEVEL) > logging.WARNING:  # WARNING is default
            self._root_logger.setLevel(env.LOG_LEVEL)
        self._root_logger.addHandler(console_out_handler)
        self._root_logger.addHandler(console_err_handler)

    def debug(
        self,
        message: str,
        /,
        *,
        extra: extra_templates.TemplateTypes | None = None,
    ) -> None:
        """
        `DEBUG` log level

        Args:
            message: message to log
            extra: extra information (use `ExtraTemplates`)
        """
        self._logger.debug(message, extra={"extra": extra})

    def info(self, message: str, /) -> None:
        """
        `INFO` log level

        Args:
            message: message to log
        """
        self._logger.info(
            message,
            stacklevel=filters.framing.INTERNAL_LOGGING_STACK_LEVEL,
        )

    def warning(
        self,
        message: str,
        /,
        *,
        exc_info: bool = False,
    ) -> None:
        """
        `WARNING` log level

        Args:
            message: message to log
            exc_info: to show exception info including stack trace (use only in except clause)
        """
        self._logger.warning(
            message,
            exc_info=exc_info,
            stacklevel=filters.framing.INTERNAL_LOGGING_STACK_LEVEL,
        )

    def error(
        self,
        message: str,
        /,
        *,
        exc_info: bool = False,
    ) -> None:
        """
        `ERROR` log level

        Args:
            message: message to log
            exc_info: to show exception info including stack trace (use only in except clause)
        """
        self._logger.error(
            message,
            exc_info=exc_info,
            stacklevel=filters.framing.INTERNAL_LOGGING_STACK_LEVEL,
        )

    def critical(
        self,
        message: str,
        /,
        *,
        exc_info: bool = False,
    ) -> None:
        """
        `CRITICAL` log level

        Args:
            message: message to log
            exc_info: to show exception info including stack trace (use only in except clause)
        """
        self._logger.critical(
            message,
            exc_info=exc_info,
            stacklevel=filters.framing.INTERNAL_LOGGING_STACK_LEVEL,
        )

    @staticmethod
    def get_request_id() -> str | None:
        return context.ctx_request_id.get()

    @staticmethod
    def set_request_id(request_id: str) -> None:
        context.ctx_request_id.set(request_id)

    @staticmethod
    def reset_request_id() -> None:
        context.ctx_request_id.set(None)

    @property
    def _root_logger(self) -> logging.Logger:
        return logging.getLogger()
