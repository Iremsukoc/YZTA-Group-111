from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from firebase_admin import auth as firebase_auth

class AuthDependencies:
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    @classmethod
    def get_current_user(cls, token: str = Depends(oauth2_scheme)):
        try:
            decoded_token = firebase_auth.verify_id_token(token, check_revoked=True)
            return decoded_token
        except firebase_auth.InvalidIdTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication token")
        except firebase_auth.UserDisabledError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User account is disabled.")
        except Exception:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")
