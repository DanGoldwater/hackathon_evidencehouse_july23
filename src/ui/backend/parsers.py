import json
import textwrap
from ..models import CostDriver, RiskFactor
from .llm_inference import create_chat_completion


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
Your job is to extract the cost drivers from the following message as a list of json objects: {output_message}.
you should give specfic estimated numbers for the min and max cost of each cost driver.
The format of the json objects should be:
[
    {{
        "title": "title of cost driver",
        "min_cost": "min cost of cost driver (int)",
        "max_cost": "max cost of cost driver (int)",
        "description": "description of cost driver"
    }},
]
ensure the answer is a valid JSON object parsable using JSON.parse(answer) return nothing else
                """
                ),
            },
        ],
    )
    output = ""
    for chunk in response:
        output += chunk
    print(output)
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
Your job is to extract all of the risk factors from the following message as a list of json objects: {output_message}.
You should give specfic numbers for the min and max cost of each risk factor.
The format of the json objects should be:
[
    {{
        "title": "title of risk factor",
        "min_cost": "min cost of risk factor (int)",
        "max_cost": "max cost of risk factor (int)",
        "description": "description of risk factor",
        "likelihood": "probability of risk factor (string)",
        "impact": "impact of risk factor (string)"
    }},
]
ensure the answer is a valid JSON object parsable using JSON.parse(answer) return nothing else

                """
                ),
            },
        ],
    )
    output = ""
    for chunk in response:
        output += chunk
    print(output)
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
                risk_probability=risk_factor.get("likelihood", None),
                impact=risk_factor.get("impact", ""),
            )
        )
    return risk_data


def parse_summary_data(output_message: str):
    pass
