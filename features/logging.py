"""Logging for Budget Basket, kept separate from business logic.

Business functions stay clean. Logging is applied with the @logged
decorator so the two concerns never mix.
"""

import functools
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)

logger = logging.getLogger("budget_basket")


def logged(func):
    """Decorator that logs when a function starts and what it returns."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info("Starting %s", func.__name__)
        result = func(*args, **kwargs)
        logger.info("Finished %s -> %r", func.__name__, result)
        return result

    return wrapper
