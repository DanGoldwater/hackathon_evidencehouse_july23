import os
import openai
import textwrap
from dotenv import load_dotenv
from typing import Generator, Union

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


def load_system_prompt() -> str:
    return "You are a data analyst in charge of assisting the UK government with procurement of contracts"


def load_intial_prompt(input_description: str) -> str:
    prompt = textwrap.dedent(
        f"""
    The UK government is doing a procurement of {input_description}. 
    Please give me a list of bullet points with key drivers of costs and key risks with this type of procurement
    Return your answer in the format:
 
    Cost Drivers (Title, MinCost (GBP), MaxCost (GBP), Description):
    ...

    Risks (Title, Description, MinCost (GBP), MaxCost (GBP), Likelihood (eg: Moderate), Impact (eg: High)):
    ...

    Summary:
    ...
    """
    )
    return prompt


def create_chat_completion(
    messages: list[dict[str, str]], model_type: str = "gpt-3.5-turbo-0613"
) -> Union[Generator, str]:
    response = openai.ChatCompletion.create(
        messages=messages,
        model=model_type,
        stream=True,
    )
    for chunk in response:
        if len(chunk["choices"][0]["delta"]) != 0:
            yield chunk["choices"][0]["delta"]["content"]
