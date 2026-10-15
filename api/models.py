from pydantic import BaseModel, Field
from typing import Optional


class ProjectCreatePayload(BaseModel):
    title: str = Field(..., min_length=2, max_length=100)
    body: str = "Automated QA test payload"
    userId: int = 1


class ProjectResponse(BaseModel):
    id: int
    title: str
    body: str
    userId: Optional[int] = None