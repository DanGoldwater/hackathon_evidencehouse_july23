import os
import openai
from typing import Generator
from .consts import MODEL_TYPE
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


def create_chat_completion(
    messages: list[dict[str, str]],
) -> Generator:
    stream = openai.ChatCompletion.create(
        messages=messages,
        model=MODEL_TYPE,
        stream=True,
    )
    for chunk in stream:
        if len(chunk["choices"][0]["delta"]) != 0:
            yield chunk["choices"][0]["delta"]["content"]
