from pydantic import BaseModel
from typing import Optional


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
