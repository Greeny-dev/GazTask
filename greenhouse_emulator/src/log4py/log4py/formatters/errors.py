from ..constants import LogFormat


class NoRealizationFound(Exception):
    def __init__(self, format_: LogFormat) -> None:
        msg_exc = f"No realization found for `{format_}`."
        super().__init__(msg_exc)
