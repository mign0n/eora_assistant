from pathlib import Path

from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole

SYS_PROMPT = Path("system_prompt.md").read_text(encoding="utf-8")

PAYLOAD = Chat(
    messages=[
        Messages(
            role=MessagesRole.SYSTEM,
            content=SYS_PROMPT,
        ),
    ],
    temperature=0.5,
    max_tokens=200,
)


async def get_answer(user_request: str, payload: Chat = PAYLOAD) -> str:
    """Receives a response from the LLM to the user's request."""
    async with GigaChat() as giga:
        payload.messages.append(
            Messages(
                role=MessagesRole.USER,
                content=user_request,
            ),
        )
        response = await giga.achat(payload)
        return response.choices[0].message.content
