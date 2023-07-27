import openai
from typing import Generator
from .consts import MODEL_TYPE


def create_chat_completion(
    messages: list[dict[str, str]],
) -> Generator:
    return openai.ChatCompletion.create(
        messages=messages,
        model=MODEL_TYPE,
        stream=True,
    )
