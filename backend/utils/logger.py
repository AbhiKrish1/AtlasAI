"""
AtlasAI

Module:
    logger.py

Responsibility:
    Configure and provide application loggers.

Dependencies:
    Python logging module

Last Updated:
    Sprint 3
"""

from __future__ import annotations

import logging

_CONFIGURED = False


def configure_logging(
    level: int = logging.INFO,
) -> None:
    """
    Configure AtlasAI logging.

    This function is idempotent and will only configure
    logging once during the application's lifetime.
    """

    global _CONFIGURED

    if _CONFIGURED:
        return

    logging.basicConfig(
        level=level,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    _CONFIGURED = True


def get_logger(
    name: str,
) -> logging.Logger:
    """
    Return a configured logger.
    """

    configure_logging()

    return logging.getLogger(name)