"""Supabase client service."""
from typing import Any, Optional
from supabase import create_client, Client
from app.config import settings


class SupabaseService:
    """Service for interacting with Supabase."""
    
    def __init__(self):
        """Initialize Supabase client."""
        if not settings.supabase_url or not settings.supabase_key:
            raise ValueError(
                "Supabase credentials not configured. Please set SUPABASE_URL and SUPABASE_KEY "
                "in your .env file or environment variables."
            )
        self.client: Client = create_client(settings.supabase_url, settings.supabase_key)
    
    async def get_user_by_id(self, user_id: str) -> Optional[dict]:
        """
        Get user by ID.
        
        Args:
            user_id: User ID
            
        Returns:
            User data or None
        """
        response = self.client.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            return response.data[0]
        return None
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        """
        Get user by email.
        
        Args:
            email: User email
            
        Returns:
            User data or None
        """
        response = self.client.table("users").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    
    async def create_user(self, user_data: dict) -> dict:
        """
        Create a new user.
        
        Args:
            user_data: User data dictionary
            
        Returns:
            Created user data
        """
        response = self.client.table("users").insert(user_data).execute()
        return response.data[0]
    
    async def update_user(self, user_id: str, user_data: dict) -> dict:
        """
        Update user data.
        
        Args:
            user_id: User ID
            user_data: User data to update
            
        Returns:
            Updated user data
        """
        response = self.client.table("users").update(user_data).eq("id", user_id).execute()
        return response.data[0]
    
    async def list_users(self) -> list[dict]:
        """
        List all users.
        
        Returns:
            List of user data
        """
        response = self.client.table("users").select("*").execute()
        return response.data
    
    async def get_cases(self, filters: Optional[dict] = None) -> list[dict]:
        """
        Get cases with optional filters.
        
        Args:
            filters: Optional filters (e.g., {"detective_id": "123"})
            
        Returns:
            List of case data
        """
        query = self.client.table("cases").select("*")
        
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        
        response = query.execute()
        return response.data
    
    async def get_case_by_id(self, case_id: str) -> Optional[dict]:
        """
        Get case by ID.
        
        Args:
            case_id: Case ID
            
        Returns:
            Case data or None
        """
        response = self.client.table("cases").select("*").eq("id", case_id).execute()
        if response.data:
            return response.data[0]
        return None
    
    async def create_case(self, case_data: dict) -> dict:
        """
        Create a new case.
        
        Args:
            case_data: Case data dictionary
            
        Returns:
            Created case data
        """
        response = self.client.table("cases").insert(case_data).execute()
        return response.data[0]
    
    async def update_case(self, case_id: str, case_data: dict) -> dict:
        """
        Update case data.
        
        Args:
            case_id: Case ID
            case_data: Case data to update
            
        Returns:
            Updated case data
        """
        case_data["updated_at"] = "now()"  # Update timestamp
        response = self.client.table("cases").update(case_data).eq("id", case_id).execute()
        return response.data[0]
    
    async def delete_case(self, case_id: str) -> bool:
        """
        Delete a case.
        
        Args:
            case_id: Case ID
            
        Returns:
            True if successful
        """
        response = self.client.table("cases").delete().eq("id", case_id).execute()
        return response.data is not None


# Global instance (will be initialized on first use or when imported)
supabase_service = None

def get_supabase_service() -> SupabaseService:
    """Get or create Supabase service instance."""
    global supabase_service
    if supabase_service is None:
        supabase_service = SupabaseService()
    return supabase_service
