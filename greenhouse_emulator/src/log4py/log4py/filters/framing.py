import inspect
import logging
import os

INTERNAL_LOGGING_STACK_LEVEL = 0  # to now waste time on internal stack frame inspecting


class Filter(logging.Filter):
    def __init__(self, outer_frame_path: str) -> None:
        self.__outer_frame_path = os.path.normcase(outer_frame_path)

    def filter(self, record: logging.LogRecord) -> bool:
        record.pathname, record.lineno, record.funcName = self.__find_caller()

        return True

    def __find_caller(self) -> tuple[str, int, str]:
        frame = inspect.currentframe()

        if frame is None:
            return "(unknown file)", 0, "(unknown function)"

        while True:
            next_f = frame.f_back

            if next_f is None:
                break

            frame = next_f

            filename = os.path.normcase(frame.f_code.co_filename)

            if filename == self.__outer_frame_path:
                frame = frame.f_back
                break

        co = frame.f_code

        return co.co_filename, frame.f_lineno, co.co_name
