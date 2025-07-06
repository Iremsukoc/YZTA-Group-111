from fastapi import APIRouter, HTTPException, status
from schemas.user import UserCreate 
from core.firebase_config import auth as firebase_auth
from core.firebase_config import db
from google.cloud import firestore

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def create_user(user_data: UserCreate):

    try:
        created_user = firebase_auth.create_user(
            email=user_data.email,
            password=user_data.password
        )
        user_info = {
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        db.collection('users').document(created_user.uid).set(user_info)
        return {"message": "User created successfully", "uid": created_user.uid}
    except firebase_auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="This email address is already in use.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"An error occurred while creating a user: {e}")