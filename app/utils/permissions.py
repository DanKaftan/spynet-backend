"""Role-based permission utilities."""
from typing import Literal
from fastapi import HTTPException, status
from app.models.user import UserResponse


Role = Literal["detective", "manager"]


def require_role(user_role: str, allowed_roles: list[Role]) -> bool:
    """
    Check if user has required role.
    
    Args:
        user_role: The user's role
        allowed_roles: List of allowed roles
        
    Returns:
        True if user has required role
        
    Raises:
        HTTPException: If user doesn't have required role
    """
    if user_role not in allowed_roles:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Insufficient permissions"
        )
    return True


def require_manager(user_role: str) -> bool:
    """Require manager role."""
    return require_role(user_role, ["manager"])


def require_detective_or_manager(user_role: str) -> bool:
    """Require detective or manager role."""
    return require_role(user_role, ["detective", "manager"])
