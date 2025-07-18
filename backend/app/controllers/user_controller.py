from fastapi import APIRouter, Depends
from app.core.dependencies import AuthDependencies

class UserController:
    def __init__(self):
        self.router = APIRouter(
            prefix="/users",
            tags=["Authentication & Users"]
        )
        self.router.add_api_route(
            path="/profile",
            endpoint=self.read_user_profile,
            methods=["GET"],
        )

    async def read_user_profile(self, current_user: dict = Depends(AuthDependencies.get_current_user)):
        return {"user_profile": current_user}
