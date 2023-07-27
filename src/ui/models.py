from pydantic import BaseModel


class RiskFactor(BaseModel):
    title: str
    description: str
    risk_probability: str
    cost_gbp: float


class CostDriver(BaseModel):
    title: str
    description: str
    cost_gbp: float
