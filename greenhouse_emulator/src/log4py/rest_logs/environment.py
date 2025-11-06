import os

REST4PY_MAXIMUM_BODY_LOG_SIZE = int(
    os.environ.get(
        "REST4PY_MAXIMUM_BODY_LOG_SIZE",
        100 * 2**10,  # 100 Kb
    )
)
