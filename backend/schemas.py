from pydantic import BaseModel


class TripRequest(BaseModel):
    destination: str
    days: int
    budget: float
    travel_style: str | None = None


class TripUpdateRequest(BaseModel):
    budget: float


class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class QuestionRequest(BaseModel):
    """Request model for Knowledge Base query"""
    question: str


class AssistantResponse(BaseModel):
    """Response model for RAG-based assistant"""
    question: str
    answer: str
    sources: list = []


class SourceReference(BaseModel):
    """Citation/Source reference from Knowledge Base"""
    document: str
    source: str
