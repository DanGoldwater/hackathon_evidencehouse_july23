from fastapi import FastAPI, HTTPException, Path
import openai
import json
import textwrap
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.responses import StreamingResponse
from llm import create_chat_completion
from llm import load_system_prompt, load_intial_prompt


app = FastAPI()

# Example data (Replace this with a database or other data storage in a real app)


class RiskFactor(BaseModel):
    title: str
    description: str
    risk_probability: Optional[str]
    min_cost: Optional[float]
    max_cost: Optional[float]


class CostDriver(BaseModel):
    title: str
    description: str
    min_cost: Optional[float]
    max_cost: Optional[float]


class ChatInput(BaseModel):
    prompt: str


chat_history = [
    {
        "role": "system",
        "content": load_system_prompt(),
    }
]


@app.post("/chat")
def chat(chat_input: ChatInput):
    if len(chat_history) == 1:
        # Add the instruction prompt if it the first one
        chat_history.append(
            {
                "role": "user",
                "content": load_intial_prompt(chat_input.prompt),
            }
        )
    else:
        # Otherwise just add the user input
        chat_history.append(
            {
                "role": "user",
                "content": chat_input.prompt,
            }
        )

    response = openai.ChatCompletion.create(
        messages=chat_history,
        model="gpt-3.5-turbo-0613",
        stream=True,
    )
    return response


@app.post("/parse_cost_drivers")
def parse_cost_drivers_data(output_message: str) -> list[CostDriver]:
    response = create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a data analyst in charge of assisting the UK government with procurement of contracts",
            },
            {
                "role": "user",
                "content": textwrap.dedent(
                    f"""
                Your job is to extract the cost drivers from this message as a list of json objects: {output_message}.
                The format of the json objects should be:
                [
                    {{
                        "title": "title of cost driver",
                        "min_cost": "min cost of cost driver (float)",
                        "max_cost": "max cost of cost driver (float)",
                        "description": "description of cost driver"
                    }},
                ]
                ensure the answer is parsable using json.loads(answer) return nothing else
                """
                ),
            },
        ],
    )
    output = ""
    for chunk in response:
        output += chunk
    cost_drivers = []
    output = json.loads(output)
    for cost_driver in output:
        if type(cost_driver.get("min_cost", "")) is str:
            cost_driver["min_cost"] = None
        if type(cost_driver.get("max_cost", "")) is str:
            cost_driver["max_cost"] = None
        cost_drivers.append(
            CostDriver(
                title=cost_driver["title"],
                min_cost=cost_driver["min_cost"],
                max_cost=cost_driver["max_cost"],
                description=cost_driver["description"],
            )
        )
    return cost_drivers


@app.post("/parse_risk_factors")
def parse_risk_factors_data(output_message: str):
    response = create_chat_completion(
        messages=[
            {
                "role": "system",
                "content": "You are a data analyst in charge of assisting the UK government with procurement of contracts",
            },
            {
                "role": "user",
                "content": textwrap.dedent(
                    f"""
                Your job is to extract the risk factors from this message as a list of json objects: {output_message}.
                The format of the json objects should be:
                [
                    {{
                        "title": "title of risk factor",
                        "min_cost": "min cost of risk factor (float)",
                        "max_cost": "max cost of risk factor (float)",
                        "description": "description of risk factor",
                        "probability": "probability of risk factor"
                    }},
                ]
                ensure the answer is parsable using json.loads(answer) return nothing else
                """
                ),
            },
        ],
    )
    output = ""
    for chunk in response:
        output += chunk
    output = json.loads(output)
    risk_data = []
    for i, risk_factor in enumerate(output):
        if type(risk_factor.get("min_cost", "")) is str:
            risk_factor["min_cost"] = None
        if type(risk_factor.get("max_cost", "")) is str:
            risk_factor["max_cost"] = None
        risk_data.append(
            RiskFactor(
                title=risk_factor["title"],
                min_cost=risk_factor["min_cost"],
                max_cost=risk_factor["max_cost"],
                description=risk_factor["description"],
                risk_probability=risk_factor.get("probability", None),
            )
        )

    return risk_data


def parse_summary_data(output_message: str):
    pass
