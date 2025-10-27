"""User models for request/response validation."""
from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user model."""
    name: str
    email: EmailStr
    role: Literal["detective", "manager"]


class UserCreate(UserBase):
    """User creation model."""
    password: str


class UserResponse(UserBase):
    """User response model."""
    id: str
    manager_id: Optional[str] = None  # Assigned manager ID
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserUpdate(BaseModel):
    """User update model."""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    role: Optional[Literal["detective", "manager"]] = None
    manager_id: Optional[str] = None  # Assign detective to manager
