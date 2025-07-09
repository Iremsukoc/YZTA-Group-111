from fastapi import APIRouter, HTTPException, status
from dto.user_dto import CreateUserDTO
from services.auth_service import register_new_user
from firebase_admin import auth

router = APIRouter(
    prefix="/users",
    tags=["Authentication & Users"]
)

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register_user_endpoint(user_data: CreateUserDTO):

    try:
        created_user = register_new_user(user_data)
        return {"message": "User registered successfully", "uid": created_user.uid}
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