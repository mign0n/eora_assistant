import logging
from pathlib import Path

from aiogram import Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from gigachat.models import Chat, Messages, MessagesRole

from config import ENCODING, SYS_PROMPT_PATH
from exceptions import APIRequestError
from services import get_answer

INTERNAL_ERROR_MESSAGE = (
    "Произошла внутренняя ошибка. Обратитесь в службу поддержки."
)
TYPE_ERROR_MESSAGE = "Ошибка типа отправляемого сообщения: {error}"

WELCOME_MESSAGE = "Здравствуйте, {name}!"

PAYLOAD = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content=Path(SYS_PROMPT_PATH).read_text(encoding=ENCODING),
        ),
    ],
    temperature=0.5,
    max_tokens=200,
)

dispatcher = Dispatcher()


@dispatcher.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """Handles the `/start` command from user, greeting him."""
    await message.answer(
        WELCOME_MESSAGE.format(name=html.bold(message.from_user.full_name)),
    )


@dispatcher.message()
async def ai_answer_handler(message: Message, payload: Chat = PAYLOAD) -> None:
    """Handles message from user, sends a response from the LLM."""
    try:
        await message.reply(
            await get_answer(message.text or "", payload=payload),
        )
    except APIRequestError:
        await message.answer(INTERNAL_ERROR_MESSAGE)
    except TypeError as error:
        logging.error(TYPE_ERROR_MESSAGE.format(error=error), exc_info=True)
        await message.answer(INTERNAL_ERROR_MESSAGE)
