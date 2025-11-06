import os

from .constants import LogFormat, LogLevel, LogVerbosity

LOG_FORMAT = LogFormat(os.environ.get("LOG_FORMAT", LogFormat.JSON))
LOG_LEVEL = LogLevel(os.environ.get("LOG_LEVEL", LogLevel.INFO))
LOG_VERBOSITY = LogVerbosity(os.environ.get("LOG_VERBOSITY", LogVerbosity.HIGH))
