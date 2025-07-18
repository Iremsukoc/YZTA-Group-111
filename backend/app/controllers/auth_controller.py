from fastapi import APIRouter, HTTPException, status, Depends, Header
from firebase_admin import auth
from app.services.auth_service import AuthService
from app.dto.auth.register_dto import RegisterDTO
from app.dto.auth.login_dto import LoginDTO
from typing import Optional

class AuthController:
    def __init__(self):
        self.router = APIRouter(
            prefix="/auth",
            tags=["Authentication"]
        )
        self.auth_service = AuthService()

        self.router.add_api_route(
            path="/register",
            endpoint=self.register_user,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )
        
        self.router.add_api_route(
            path="/login",
            endpoint=self.login_user,
            methods=["POST"],
        )
        
        self.router.add_api_route(
            path="/refresh",
            endpoint=self.refresh_token,
            methods=["POST"],
        )
        
        self.router.add_api_route(
            path="/verify",
            endpoint=self.verify_token,
            methods=["GET"],
        )
        
        self.router.add_api_route(
            path="/logout",
            endpoint=self.logout_user,
            methods=["POST"],
        )
        
        self.router.add_api_route(
            path="/me",
            endpoint=self.get_current_user,
            methods=["GET"],
        )

    async def register_user(self, user_data: RegisterDTO):
        try:
            token_response = self.auth_service.register_new_user(user_data)
            return {
                "message": "User registered successfully",
                "data": {
                    "custom_token": token_response["custom_token"],
                    "user_id": token_response["user_id"]
                }
            }
        except auth.EmailAlreadyExistsError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="This email address is already in use."
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An unexpected error occurred: {str(e)}"
            )
    
    async def login_user(self, login_data: LoginDTO):
        try:
            tokens = self.auth_service.login_user(login_data.email, login_data.password)
            return {
                "message": "Login successful",
                "data": {
                    "access_token": tokens["access_token"],
                    "refresh_token": tokens["refresh_token"],
                    "custom_token": tokens["custom_token"],
                    "user_id": tokens["user_id"],
                    "user_data": tokens["user_data"]
                }
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Login failed: {str(e)}"
            )

    async def refresh_token(self, request_body: dict):
        try:
            refresh_token = request_body.get("refresh_token")
            if not refresh_token:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Refresh token is required"
                )
            
            tokens = self.auth_service.refresh_token(refresh_token)
            return {
                "message": "Token refreshed successfully",
                "data": tokens
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token refresh failed: {str(e)}"
            )

    async def verify_token(self, authorization: Optional[str] = Header(None)):
        try:
            if not authorization:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header is required"
                )
            
            if not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header format"
                )
            
            token = authorization.split(" ")[1]
            decoded_token = self.auth_service.verify_token(token)
            
            return {
                "message": "Token is valid",
                "data": {
                    "user_id": decoded_token.get("uid"),
                    "email": decoded_token.get("email"),
                    "exp": decoded_token.get("exp"),
                    "iat": decoded_token.get("iat")
                }
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token verification failed: {str(e)}"
            )

    async def logout_user(self, authorization: Optional[str] = Header(None)):
        try:
            if not authorization:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header is required"
                )
            
            if not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header format"
                )
            
            token = authorization.split(" ")[1]
            decoded_token = self.auth_service.verify_token(token)
            user_id = decoded_token.get("uid")
            
            result = self.auth_service.logout_user(user_id)
            return {
                "message": result["message"]
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Logout failed: {str(e)}"
            )

    async def get_current_user(self, authorization: Optional[str] = Header(None)):
        try:
            if not authorization:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authorization header is required"
                )
            
            if not authorization.startswith("Bearer "):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authorization header format"
                )
            
            token = authorization.split(" ")[1]
            decoded_token = self.auth_service.verify_token(token)
            user_id = decoded_token.get("uid")
            
            user_data = self.auth_service.get_user_by_id(user_id)
            
            return {
                "message": "User data retrieved successfully",
                "data": user_data
            }
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Failed to get user data: {str(e)}"
            )

    async def get_current_user_dependency(authorization: Optional[str] = Header(None)):
        if not authorization:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header is required"
            )
        
        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )
        
        try:
            token = authorization.split(" ")[1]
            auth_service = AuthService()
            decoded_token = auth_service.verify_token(token)
            return decoded_token
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Token verification failed: {str(e)}"
            )