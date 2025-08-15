import asyncio
import logging

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError

from config import configure_logging, load_config
from handlers import dispatcher

INVALID_TOKEN_ERROR_MESSAGE = "Недействительный токен: {error}"
UNEXPECTED_ERROR_MESSAGE = "Неожиданный сбой приложения: {error}"


async def main() -> None:
    """Main function."""
    config = load_config()
    try:
        await dispatcher.start_polling(
            Bot(
                token=config.bot.token.get_secret_value(),
                default=DefaultBotProperties(parse_mode=ParseMode.HTML),
            ),
        )
    except TelegramUnauthorizedError as error:
        logging.error(
            INVALID_TOKEN_ERROR_MESSAGE.format(error=error),
            exc_info=True,
        )
    except Exception as error:
        logging.error(
            UNEXPECTED_ERROR_MESSAGE.format(error=error),
            exc_info=True,
        )


if __name__ == "__main__":
    configure_logging()
    asyncio.run(main())
