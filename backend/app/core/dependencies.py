from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth as firebase_auth

bearer_scheme = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer token not found",
        )
        
    token = credentials.credentials
    try:
        decoded_token = firebase_auth.verify_id_token(token, check_revoked=True)
        return decoded_token
    except firebase_auth.InvalidIdTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid authentication token"
        )
    except firebase_auth.UserDisabledError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="User account is disabled."
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    
CurrentUser = Depends(get_current_user)
