import sys

from loguru import logger


class Trace:
    def __init__(
        self,
    ):
        self.logger = logger

        self.logger.remove()

        self.logger.add(
            sys.stdout,
            colorize=True,
            level="INFO",
        )
