from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv
from environs import Env


@dataclass
class EnvironmentVariables:
    DATABASE_DSN: str
    FLASK_PORT: str
    FLASK_DEBUG: str
    FLASK_APP: str
    FLASK_ENV: str
    PACKAGE_NAME: str
    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool
    SQLALCHEMY_ECHO: bool
    API_KEY: str


class Environment:
    """Environment class"""

    def __init__(self, dotenv_path: Optional[str] = ".env"):
        load_dotenv(dotenv_path)
        self._env = Env()

    def get(self, key: str) -> str:
        """Get environment variable"""

        value = self._env.str(key)

        if not value:
            raise ValueError(f"Environment variable {key} not found")

        return value

    def load(self) -> EnvironmentVariables:
        """Load environment variables from dict"""
        return EnvironmentVariables(
            DATABASE_DSN=self.get("DATABASE_DSN"),
            FLASK_PORT=self.get("FLASK_PORT"),
            FLASK_DEBUG=self.get("FLASK_DEBUG"),
            FLASK_ENV=self.get("FLASK_ENV"),
            FLASK_APP=self.get("FLASK_APP"),
            PACKAGE_NAME=self.get("PACKAGE_NAME"),
            SQLALCHEMY_DATABASE_URI=self.get("SQLALCHEMY_DATABASE_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=self.get("SQLALCHEMY_TRACK_MODIFICATIONS"),
            SQLALCHEMY_ECHO=self.get("SQLALCHEMY_ECHO"),
            API_KEY=self.get("API_KEY"),
        )
