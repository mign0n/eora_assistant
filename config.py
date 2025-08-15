import logging

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'


def configure_logging():
    """Configures the logger."""
    logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
    )
