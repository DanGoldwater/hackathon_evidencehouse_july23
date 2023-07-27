from pydantic import BaseModel


class RiskFactor(BaseModel):
    title: str
    description: str
    risk_probability: str
    cost_increase_millions: float
