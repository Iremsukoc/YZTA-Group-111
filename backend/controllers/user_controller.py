from fastapi import APIRouter, Depends
from core.dependencies import get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Authentication & Users"]
)

@router.get("/profile", dependencies=[Depends(get_current_user)])
def read_user_profile(current_user: dict = Depends(get_current_user)):
    
    return {"user_profile": current_user}