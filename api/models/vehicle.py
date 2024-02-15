from typing import List, Optional

from pydantic import BaseModel


class Description(BaseModel):
    short: str
    long: Optional[str] = None


class Feature(BaseModel):
    feature: str
    description: Description


class Vehicle(BaseModel):
    id: str
    features: List[Feature]
