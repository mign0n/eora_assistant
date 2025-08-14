import asyncio
import logging
import os
import sys

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from services import get_answer

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
WELCOME_MESSAGE = "Здравствуйте, {name}!"

dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Receives messages with `/start` command."""
    await message.answer(
        WELCOME_MESSAGE.format(name=html.bold(message.from_user.full_name)),
    )


@dp.message()
async def ai_answer_handler(message: Message) -> None:
    """Receives answer from AI."""
    answer_text = await get_answer(message.text or "")
    try:
        await message.reply(answer_text)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    """Main function."""
    await dp.start_polling(
        Bot(
            token=BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        ),
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
