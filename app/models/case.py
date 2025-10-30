"""Case models for request/response validation."""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel


class CaseBase(BaseModel):
    """Base case model."""
    title: str
    details: str
    location: str
    status: Literal["open", "in_progress", "closed"] = "open"


class CaseCreate(CaseBase):
    """Case creation model."""
    detective_id: Optional[str] = None  # Assigned detective (optional)
    # manager_id is set automatically from the authenticated manager creating the case


class CaseUpdate(BaseModel):
    """Case update model."""
    title: Optional[str] = None
    details: Optional[str] = None
    location: Optional[str] = None
    status: Optional[Literal["open", "in_progress", "closed"]] = None
    detective_id: Optional[str] = None


class CaseResponse(CaseBase):
    """Case response model."""
    id: str
    detective_id: Optional[str]
    manager_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
