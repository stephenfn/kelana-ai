from pydantic import BaseModel


class TripRequest(BaseModel):
    destination: str
    days: int
    budget: float


class TripUpdateRequest(BaseModel):
    budget: float