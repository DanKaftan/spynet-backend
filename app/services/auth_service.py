"""Authentication service using Supabase Auth."""
from typing import Optional
from fastapi import HTTPException, status
from supabase import Client
from app.config import settings
from app.services.supabase_service import supabase_service


class AuthService:
    """Service for handling authentication."""
    
    def __init__(self):
        """Initialize auth service with Supabase client."""
        self.client: Client = supabase_service.client
    
    async def signup(self, email: str, password: str, name: str, role: str) -> dict:
        """
        Sign up a new user.
        
        Args:
            email: User email
            password: User password
            name: User name
            role: User role (detective or manager)
            
        Returns:
            User data and access token
            
        Raises:
            HTTPException: If signup fails
        """
        try:
            # Create auth user
            auth_response = self.client.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if not auth_response.user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Failed to create user"
                )
            
            user_id = auth_response.user.id
            
            # Create user profile in database
            user_data = {
                "id": user_id,
                "name": name,
                "email": email,
                "role": role
            }
            
            created_user = await supabase_service.create_user(user_data)
            
            return {
                "user": created_user,
                "access_token": auth_response.session.access_token if auth_response.session else None
            }
            
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Signup failed: {str(e)}"
            )
    
    async def login(self, email: str, password: str) -> dict:
        """
        Login user and return JWT token.
        
        Args:
            email: User email
            password: User password
            
        Returns:
            User data and access token
            
        Raises:
            HTTPException: If login fails
        """
        try:
            auth_response = self.client.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if not auth_response.user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid credentials"
                )
            
            user_id = auth_response.user.id
            
            # Get user profile from database
            user = await supabase_service.get_user_by_id(user_id)
            
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User profile not found"
                )
            
            return {
                "user": user,
                "access_token": auth_response.session.access_token
            }
            
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Login failed: {str(e)}"
            )
    
    async def get_user_from_token(self, token: str) -> Optional[dict]:
        """
        Get user data from JWT token.
        
        Args:
            token: JWT token
            
        Returns:
            User data or None
        """
        try:
            # Verify token and get user
            auth_response = self.client.auth.get_user(token)
            
            if not auth_response.user:
                return None
            
            user_id = auth_response.user.id
            return await supabase_service.get_user_by_id(user_id)
            
        except Exception:
            return None


# Global instance
auth_service = AuthService()
