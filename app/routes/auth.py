"""Authentication routes."""
from typing import Optional
from fastapi import APIRouter, HTTPException, status
from app.models.user import UserCreate, UserResponse
from app.services.auth_service import auth_service
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])


class LoginRequest(BaseModel):
    """Login request model."""
    email: str
    password: str


class AuthResponse(BaseModel):
    """Authentication response model."""
    user: dict
    access_token: Optional[str] = None  # Optional if email confirmation is required


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: UserCreate):
    """
    Sign up a new user.
    
    - **email**: User email
    - **password**: User password
    - **name**: User name
    - **role**: User role (detective or manager)
    
    Returns user data and JWT token.
    """
    try:
        result = await auth_service.signup(
            email=user.email,
            password=user.password,
            name=user.name,
            role=user.role
        )
        return AuthResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        error_msg = str(e) if str(e) else repr(e)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Signup failed: {error_msg}"
        )


@router.post("/login", response_model=AuthResponse, status_code=status.HTTP_200_OK)
async def login(credentials: LoginRequest):
    """
    Login user and return JWT token.
    
    - **email**: User email
    - **password**: User password
    
    Returns user data and JWT token.
    """
    try:
        result = await auth_service.login(
            email=credentials.email,
            password=credentials.password
        )
        return AuthResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e)
        )
