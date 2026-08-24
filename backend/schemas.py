from pydantic import BaseModel


class TripRequest(BaseModel):
    destination: str
    days: int
    budget: float
    travel_style: str | None = None


class TripUpdateRequest(BaseModel):
    budget: float