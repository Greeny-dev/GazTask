import os

from api_server import create_app, start_api_server
from log4py import logger


def main() -> int:
    try:
        app = create_app()
    except Exception:
        msg_crit = "Error during service's initialization. Check configs."
        logger.critical(msg_crit)
        return 1

    host = os.getenv("API_SERVER_HOST")
    port = int(os.getenv("API_SERVER_PORT"))

    start_api_server(
        app,
        host=host,
        port=port,
    )

    return 0


if __name__ == "__main__":
    exit_code = main()

    os._exit(exit_code)
