from fastapi import APIRouter, Depends, HTTPException, status
from api.v1.dependencies import get_current_user
from core.firebase_config import db

router = APIRouter()

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
   
    uid = current_user.get("uid")
    try:
        user_doc = db.collection('users').document(uid).get()
        if user_doc.exists:
            return user_doc.to_dict()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user was not found in the database.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))