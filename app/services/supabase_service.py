"""Supabase client service."""
from typing import Any, Optional, List
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
        response = self.client.table("users").select("*").eq("id", user_id).execute()
        if response.data:
            return response.data[0]
        return None
    
    async def get_user_by_email(self, email: str) -> Optional[dict]:
        response = self.client.table("users").select("*").eq("email", email).execute()
        if response.data:
            return response.data[0]
        return None
    
    async def create_user(self, user_data: dict) -> dict:
        response = self.client.table("users").insert(user_data).execute()
        return response.data[0]
    
    async def update_user(self, user_id: str, user_data: dict) -> dict:
        response = self.client.table("users").update(user_data).eq("id", user_id).execute()
        return response.data[0]
    
    async def list_users(self) -> list[dict]:
        response = self.client.table("users").select("*").execute()
        return response.data

    # ===== M2M Assignments =====
    async def assign_detective_to_manager(self, detective_id: str, manager_id: str) -> bool:
        self.client.table("detective_manager").insert({
            "manager_id": manager_id,
            "detective_id": detective_id
        }).execute()
        return True

    async def unassign_detective_from_manager(self, detective_id: str, manager_id: str) -> bool:
        self.client.table("detective_manager").delete().match({
            "manager_id": manager_id,
            "detective_id": detective_id
        }).execute()
        return True

    async def get_detectives_for_manager(self, manager_id: str) -> list[dict]:
        # Join detective_manager -> users on detectives
        # First fetch detective ids
        dm = self.client.table("detective_manager").select("detective_id").eq("manager_id", manager_id).execute()
        ids = [row["detective_id"] for row in (dm.data or [])]
        if not ids:
            return []
        res = self.client.table("users").select("*").in_("id", ids).execute()
        return res.data or []

    async def get_managers_for_detective(self, detective_id: str) -> list[dict]:
        dm = self.client.table("detective_manager").select("manager_id").eq("detective_id", detective_id).execute()
        ids = [row["manager_id"] for row in (dm.data or [])]
        if not ids:
            return []
        res = self.client.table("users").select("*").in_("id", ids).execute()
        return res.data or []

    # ===== Cases =====
    async def get_cases(self, filters: Optional[dict] = None) -> list[dict]:
        query = self.client.table("cases").select("*")
        if filters:
            for key, value in filters.items():
                query = query.eq(key, value)
        response = query.execute()
        return response.data

    async def get_unassigned_cases_by_manager(self, manager_id: str, status: Optional[str] = None) -> list[dict]:
        query = self.client.table("cases").select("*").eq("manager_id", manager_id).is_("detective_id", "null")
        if status:
            query = query.eq("status", status)
        response = query.execute()
        return response.data

    async def get_unassigned_cases_by_managers(self, manager_ids: List[str], status: Optional[str] = None) -> list[dict]:
        if not manager_ids:
            return []
        query = self.client.table("cases").select("*").in_("manager_id", manager_ids).is_("detective_id", "null")
        if status:
            query = query.eq("status", status)
        response = query.execute()
        return response.data

    async def get_case_by_id(self, case_id: str) -> Optional[dict]:
        response = self.client.table("cases").select("*").eq("id", case_id).execute()
        if response.data:
            return response.data[0]
        return None
    
    async def create_case(self, case_data: dict) -> dict:
        response = self.client.table("cases").insert(case_data).execute()
        return response.data[0]
    
    async def update_case(self, case_id: str, case_data: dict) -> dict:
        case_data["updated_at"] = "now()"
        response = self.client.table("cases").update(case_data).eq("id", case_id).execute()
        return response.data[0]
    
    async def delete_case(self, case_id: str) -> bool:
        response = self.client.table("cases").delete().eq("id", case_id).execute()
        return response.data is not None


# Global instance (will be initialized on first use or when imported)
supabase_service = None

def get_supabase_service() -> SupabaseService:
    global supabase_service
    if supabase_service is None:
        supabase_service = SupabaseService()
    return supabase_service
