from fastapi import APIRouter
from app.core.dependencies import CurrentUser
from app.dto.user.user_dto import UpdateUserProfileDTO
from app.services.user_service import UserService 
from app.services.auth_service import AuthService 

class UserController:
    def __init__(self):
        self.router = APIRouter(prefix="/users", tags=["Users"])
        self.user_service = UserService()
        self.auth_service = AuthService() 

        self.router.add_api_route("/me", self.get_current_user_profile, methods=["GET"])
        self.router.add_api_route("/me", self.update_user_profile, methods=["PUT"])
        self.router.add_api_route("/me/change-password", self.change_password, methods=["POST"])
        self.router.add_api_route("/me", self.delete_account, methods=["DELETE"])
    
    async def get_current_user_profile(self, current_user: dict = CurrentUser):
        return {"user_profile": current_user}

    async def update_user_profile(self, profile_data: UpdateUserProfileDTO, current_user: dict = CurrentUser):
        user_id = current_user.get("uid")
        updated_profile = self.user_service.update_profile(user_id, profile_data)
        return {"message": "Profile updated successfully", "data": updated_profile}

    async def change_password(self, password_data: dict, current_user: dict = CurrentUser):
        # Burada ChangePasswordDTO kullanılmalı, şimdilik basit tuttum
        user_id = current_user.get("uid")
        result = self.auth_service.change_password(user_id, password_data.get("new_password"))
        return result

    async def delete_account(self, current_user: dict = CurrentUser):
        user_id = current_user.get("uid")
        result = self.auth_service.delete_user_account(user_id)
        return result
