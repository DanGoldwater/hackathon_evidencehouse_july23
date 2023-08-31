from typing import Optional

from pydantic import BaseModel


class RiskFactor(BaseModel):
    title: str
    description: str
    risk_probability: Optional[str]
    min_cost: Optional[float]
    max_cost: Optional[float]
    impact: str


class CostDriver(BaseModel):
    title: str
    description: str
    min_cost: Optional[float]
    max_cost: Optional[float]
