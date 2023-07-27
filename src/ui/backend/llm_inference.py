import os
import openai
import textwrap
from typing import Generator
from .consts import MODEL_TYPE
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


def load_system_prompt() -> str:
    return "You are a data analyst in charge of assisting the UK government with procurement of contracts"


def load_intial_prompt(input_description: str) -> str:
    prompt = textwrap.dedent(
        f"""
    The UK government is doing a procurement of {input_description}. 
    Please give me a list of bullet points with key drivers of costs and key risks with this type of procurement"""
    )
    return prompt


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
