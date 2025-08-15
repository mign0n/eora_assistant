import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramUnauthorizedError
from aiogram.filters import CommandStart
from aiogram.types import Message

from config import configure_logging
from exceptions import APIRequestError
from services import get_answer

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WELCOME_MESSAGE = "Здравствуйте, {name}!"

INTERNAL_ERROR_MESSAGE = (
    "Произошла внутренняя ошибка. Обратитесь в службу поддержки."
)
INVALID_TOKEN_ERROR_MESSAGE = "Недействительный токен: {error}"
TYPE_ERROR_MESSAGE = "Ошибка типа отправляемого сообщения: {error}"
UNEXPECTED_ERROR_MESSAGE = "Неожиданный сбой приложения: {error}"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handles the `/start` command from user, greeting him."""
    await message.answer(
        WELCOME_MESSAGE.format(name=html.bold(message.from_user.full_name)),
    )


@dp.message()
async def ai_answer_handler(message: Message) -> None:
    """Handles message from user, sends a response from the LLM."""
    try:
        await message.reply(await get_answer(message.text or ""))
    except APIRequestError:
        await message.answer(INTERNAL_ERROR_MESSAGE)
    except TypeError as error:
        logging.error(TYPE_ERROR_MESSAGE.format(error=error), exc_info=True)
        await message.answer(INTERNAL_ERROR_MESSAGE)


async def main() -> None:
    """Main function."""
    try:
        await dp.start_polling(
            Bot(
                token=BOT_TOKEN,
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
