from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from environs import Env


@dataclass
class AppConfig:
    DATABASE_URL: str
    FLASK_PORT: str
    FLASK_DEBUG: str
    FLASK_APP: str
    PACKAGE_NAME: str


class Environment:
    """Environment class"""

    def __init__(self, dotenv_path: Optional[str] = ".env"):
        load_dotenv(dotenv_path)
        self.env = Env()

        self.app_config = AppConfig(
            DATABASE_URL=self.env.str("DATABASE_URL"),
            FLASK_PORT=self.env.str("FLASK_PORT"),
            FLASK_DEBUG=self.env.str("FLASK_DEBUG"),
            FLASK_APP=self.env.str("FLASK_APP"),
            PACKAGE_NAME=self.env.str("PACKAGE_NAME"),
        )

    def get(self, key: str) -> Optional[str]:
        """Get environment variable"""
        value = getattr(self.app_config, key, None)

        if value is None:
            raise Exception(f"Environment variable {key} not found.")

        return value
