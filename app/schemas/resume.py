from pydantic import BaseModel
from typing import List, Optional


class ResumeData(BaseModel):
    filename: str
    name: Optional[str]
    email: Optional[str]
    phone: Optional[str]
    skills: List[str]


class ResumeResponse(BaseModel):
    success: bool
    message: str
    data: ResumeData
