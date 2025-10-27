"""Case routes."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from app.models.case import CaseCreate, CaseResponse, CaseUpdate
from app.middleware import get_current_user
from app.utils.permissions import require_manager, require_detective_or_manager
from app.services.supabase_service import get_supabase_service

router = APIRouter(prefix="/cases", tags=["Cases"])


@router.get("", response_model=List[CaseResponse], status_code=status.HTTP_200_OK)
async def list_cases(
    current_user: dict = Depends(get_current_user),
    case_status: Optional[str] = Query(None, alias="status", description="Filter by status"),
    detective_id: Optional[str] = Query(None, description="Filter by detective ID")
):
    """
    List cases.
    
    - **status**: Filter by case status (optional)
    - **detective_id**: Filter by detective ID (optional)
    
    Returns all cases for managers, or only cases assigned to the logged-in detective.
    """
    try:
        require_detective_or_manager(current_user.get("role"))
        
        user_role = current_user.get("role")
        filters = {}
        
        # Detectives only see their own cases
        if user_role == "detective":
            filters["detective_id"] = current_user.get("id")
        elif detective_id:
            filters["detective_id"] = detective_id
        
        # Add status filter if provided
        if case_status:
            filters["status"] = case_status
        
        cases = await get_supabase_service().get_cases(filters)
        return cases
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve cases: {str(e)}"
        )


@router.get("/{case_id}", response_model=CaseResponse, status_code=status.HTTP_200_OK)
async def get_case(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get case by ID.
    
    - **case_id**: Case ID
    
    Returns case details.
    Detectives can only view their own cases unless they're managers.
    """
    try:
        require_detective_or_manager(current_user.get("role"))
        
        case = await get_supabase_service().get_case_by_id(case_id)
        
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found"
            )
        
        # Check permissions: detectives can only view their own cases
        user_role = current_user.get("role")
        if user_role == "detective" and case.get("detective_id") != current_user.get("id"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only view your own cases"
            )
        
        return case
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to retrieve case: {str(e)}"
        )


@router.post("", response_model=CaseResponse, status_code=status.HTTP_201_CREATED)
async def create_case(
    case: CaseCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new case (manager only).
    
    - **case**: Case data to create
    
    Creates a new case and optionally assigns it to a detective.
    """
    try:
        require_manager(current_user.get("role"))
        
        case_data = case.dict(exclude_none=True)
        
        # If no detective_id is provided, it's unassigned
        created_case = await get_supabase_service().create_case(case_data)
        return created_case
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create case: {str(e)}"
        )


@router.put("/{case_id}", response_model=CaseResponse, status_code=status.HTTP_200_OK)
async def update_case(
    case_id: str,
    case_update: CaseUpdate,
    current_user: dict = Depends(get_current_user)
):
    """
    Update case by ID.
    
    - **case_id**: Case ID
    - **case_update**: Case data to update
    
    Detectives can only update status and details of their own cases.
    Managers can update all fields.
    """
    try:
        require_detective_or_manager(current_user.get("role"))
        
        # Get existing case
        case = await get_supabase_service().get_case_by_id(case_id)
        
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found"
            )
        
        user_role = current_user.get("role")
        update_data = case_update.dict(exclude_none=True)
        
        # Detectives can only update certain fields of their own cases
        if user_role == "detective":
            # Check if case is assigned to this detective
            if case.get("detective_id") != current_user.get("id"):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You can only update your own cases"
                )
            
            # Detectives can only update status and details
            allowed_fields = {"status", "details"}
            update_data = {k: v for k, v in update_data.items() if k in allowed_fields}
        
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No valid fields to update"
            )
        
        updated_case = await get_supabase_service().update_case(case_id, update_data)
        return updated_case
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update case: {str(e)}"
        )


@router.delete("/{case_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_case(case_id: str, current_user: dict = Depends(get_current_user)):
    """
    Delete case by ID (manager only).
    
    - **case_id**: Case ID
    
    Permanently deletes a case.
    """
    try:
        require_manager(current_user.get("role"))
        
        # Check if case exists
        case = await get_supabase_service().get_case_by_id(case_id)
        
        if not case:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Case not found"
            )
        
        await get_supabase_service().delete_case(case_id)
        return None
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete case: {str(e)}"
        )
