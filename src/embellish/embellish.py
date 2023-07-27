import pandas as pd

# from anthropic import Genesis
from ..vector_store import vector_store
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.environ["ANTHROPIC_API_KEY"]


import pandas as pd
import requests
import time

from anthropic import Anthropic, HUMAN_PROMPT, AI_PROMPT

PRE_PROMPT = "I am about to pass you a description of a project. Based on this description, describe three possible unforseen costs of the project. You can embellish, but be realistic. Be concise; use around ten words per point. "


def clean_up_text(input_text):
    lines = input_text.split("\n")  # split the text by newline
    cleaned_lines = [
        " ".join(line.split()) for line in lines
    ]  # for each line, split by whitespace and rejoin
    output_text = "\n".join(cleaned_lines)  # rejoin the lines with newline
    return output_text


def get_anthropic_embellishment(
    description: str,
    # pre_prompt: str
):
    pre_prompt = PRE_PROMPT
    anthropic = Anthropic()
    completion = anthropic.completions.create(
        model="claude-1",
        max_tokens_to_sample=300,
        prompt=f"{HUMAN_PROMPT} {pre_prompt} \n {description}{AI_PROMPT}",
    )
    return clean_up_text(completion.completion)


desc = "We built a thousand ships, all of them in Theseus. None looked alike"

# print(get_anthropic_embellishment(
#     description=desc,
#     pre_prompt=PRE_PROMPT
# ))


def embellish_dataframe(df: pd.DataFrame):
    df["unforseen_costs"] = df["Description"].apply(get_anthropic_embellishment)
    return df
