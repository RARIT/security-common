import logging
import sys

from .config import LOG_LEVEL


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a standardized logger.
    """

    logger_name = f"security-platform.{name}"

    logger = logging.getLogger(logger_name)

    if logger.handlers:
        return logger

    logger.setLevel(LOG_LEVEL)

    handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(
        fmt=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    logger.propagate = False

    return logger