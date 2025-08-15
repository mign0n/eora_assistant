import logging
import os
from dataclasses import dataclass

from pydantic import BaseModel, SecretStr

DATETIME_FORMAT = "%Y-%m-%d_%H-%M-%S"
ENCODING = "utf-8"
LOG_FORMAT = '"%(asctime)s - [%(levelname)s] - %(message)s"'
SYS_PROMPT_PATH = "system_prompt.md"


class BotConfig(BaseModel):
    """Bot configuration."""

    token: SecretStr


@dataclass
class Config:
    """Application configuration."""

    bot: BotConfig


def load_config() -> Config:
    """Loads application configuration."""
    return Config(bot=BotConfig(token=os.getenv("BOT_TOKEN", "")))


def configure_logging():
    """Configures the logger."""
    logging.basicConfig(
        datefmt=DATETIME_FORMAT,
        format=LOG_FORMAT,
        level=logging.INFO,
    )
