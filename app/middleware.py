"""JWT authentication middleware."""
from typing import Optional
from fastapi import Header, HTTPException, status
from app.services.auth_service import auth_service


async def get_current_user(authorization: str = Header(None)) -> dict:
    """
    Get current user from JWT token.
    
    Args:
        authorization: Authorization header with Bearer token
        
    Returns:
        Current user data
        
    Raises:
        HTTPException: If authentication fails
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization header missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from "Bearer <token>"
    try:
        scheme, token = authorization.split()
        if scheme.lower() != "bearer":
            raise ValueError()
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from token
    user = await auth_service.get_user_from_token(token)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user
