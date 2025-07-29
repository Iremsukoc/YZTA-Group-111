from fastapi import APIRouter, HTTPException, status
from app.services.auth_service import AuthService
from app.dto.auth.register_dto import RegisterDTO
from firebase_admin import auth


class AuthController:
    def __init__(self):
        self.router = APIRouter(prefix="/auth", tags=["Authentication"])
        self.auth_service = AuthService()

        self.router.add_api_route(
            path="/register",
            endpoint=self.register_user,
            methods=["POST"],
            status_code=status.HTTP_201_CREATED,
        )

    async def register_user(self, user_data: RegisterDTO):
        try:
            user = self.auth_service.register_new_user(user_data)
            return {"message": "User registered successfully", "uid": user.uid}
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