"""User routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.models.user import UserResponse, UserUpdate
from app.middleware import get_current_user
from app.utils.permissions import require_manager
from app.services.supabase_service import get_supabase_service

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def list_users(current_user: dict = Depends(get_current_user)):
    """
    List all users (manager only).
    
    Requires manager role.
    Returns list of all users.
    """
    # Check permissions
    require_manager(current_user.get("role"))
    
    try:
        users = await get_supabase_service().list_users()
        return users
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve users: {str(e)}"
        )


@router.get("/detectives", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def list_detectives(
    manager_id: Optional[str] = Query(None, description="Filter by manager ID"),
    current_user: dict = Depends(get_current_user)
):
    """
    List all detective users.
    
    - **manager_id** (optional): Filter by assigned manager ID
    
    Returns list of all users with role="detective".
    If manager_id is provided, returns only detectives assigned to that manager.
    Both detectives and managers can access this endpoint.
    """
    try:
        # Get all users and filter for detectives
        all_users = await get_supabase_service().list_users()
        detectives = [user for user in all_users if user.get("role") == "detective"]
        
        # Filter by manager if specified
        if manager_id:
            detectives = [det for det in detectives if det.get("manager_id") == manager_id]
        
        return detectives
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve detectives: {str(e)}"
        )


@router.get("/my-detectives", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_my_detectives(current_user: dict = Depends(get_current_user)):
    """
    Get detectives assigned to the logged-in manager.
    
    Returns list of detectives assigned to the current manager.
    Requires manager role.
    """
    try:
        # Check if user is a manager
        require_manager(current_user.get("role"))
        
        # Get detectives assigned to this manager
        all_users = await get_supabase_service().list_users()
        my_detectives = [
            user for user in all_users 
            if user.get("role") == "detective" and user.get("manager_id") == current_user.get("id")
        ]
        
        return my_detectives
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve your detectives: {str(e)}"
        )


@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_user(user_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get user by ID.
    
    - **user_id**: User ID
    
    Returns user details.
    """
    try:
        # Managers can view anyone, detectives can only view themselves
        if current_user.get("role") != "manager" and user_id != current_user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own profile"
            )
        
        user = await get_supabase_service().get_user_by_id(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve user: {str(e)}"
        )


@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def update_user(
    user_id: str,
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update user by ID.
    
    - **user_id**: User ID
    - **user_update**: User data to update
    
    Only managers can update other users. Users can update their own profile (name only).
    """
    try:
        # Check permissions
        can_update = False
        
        if current_user.get("role") == "manager":
            can_update = True
        elif user_id == current_user.get("id"):
            # Users can only update their own name
            update_data = user_update.dict(exclude_none=True)
            if set(update_data.keys()) <= {"name"}:
                can_update = True
        
        if not can_update:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions"
            )
        
        # Update user
        update_data = user_update.dict(exclude_none=True)
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )
        
        updated_user = await get_supabase_service().update_user(user_id, update_data)
        return updated_user
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update user: {str(e)}"
        )
