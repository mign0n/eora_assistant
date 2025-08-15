import logging

from gigachat import GigaChat
from gigachat.exceptions import ResponseError
from gigachat.models import Chat, Messages, MessagesRole
from httpx import ConnectError

from exceptions import APIRequestError

API_REQUEST_ERROR_MESSAGE = "Ошибка запроса к API LLM: {error}"


async def get_answer(user_request: str, payload: Chat) -> str:
    """Receives a response from the LLM to the user's request."""
    async with GigaChat() as giga:
        payload.messages.append(
            Messages(
                role=MessagesRole.USER,
                content=user_request,
            ),
        )
        try:
            response = await giga.achat(payload)
        except (ConnectError, ResponseError) as error:
            error_message = API_REQUEST_ERROR_MESSAGE.format(error=error)
            logging.error(error_message, exc_info=True)
            raise APIRequestError(error_message) from error

        choice, *_ = response.choices
        return choice.message.content
