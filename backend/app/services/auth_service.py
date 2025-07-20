from firebase_admin import auth as firebase_auth
from firebase_admin import firestore
from app.services.firebase_service import FirebaseService
from app.dto.auth.register_dto import RegisterDTO
from app.config.firebase_config import FIREBASE_API_KEY, FIREBASE_PROJECT_ID
import requests

class AuthService:
    def __init__(self):
        self.db = FirebaseService.get_db()
        self.collection = "users"
        self.firebase_api_key = FIREBASE_API_KEY
        self.firebase_project_id = FIREBASE_PROJECT_ID

    def register_new_user(self, user_data: RegisterDTO):
        try:
            created_user = firebase_auth.create_user(
                email=user_data.email,
                password=user_data.password,
                display_name=f"{user_data.first_name} {user_data.last_name}"
            )

            user_info = {
                "first_name": user_data.first_name,
                "last_name": user_data.last_name,
                "email": user_data.email,
                "created_at": firestore.SERVER_TIMESTAMP
            }

            self.db.collection(self.collection).document(created_user.uid).set(user_info)

            custom_claims = {
                "personId": created_user.uid,
                "firstName": user_data.first_name,
                "lastName": user_data.last_name,
                "email": user_data.email
            }
            firebase_auth.set_custom_user_claims(created_user.uid, custom_claims)

            custom_token = firebase_auth.create_custom_token(created_user.uid, custom_claims)

            return {
                "custom_token": custom_token.decode('utf-8'),
                "user_id": created_user.uid
            }
        except Exception as e:
            raise RuntimeError(f"An error occurred during user registration: {str(e)}")

    def login_user(self, email: str, password: str):
        print("Using Firebase API Key:", self.firebase_api_key)

        try:
            auth_url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={self.firebase_api_key}"
            
            payload = {
                "email": email,
                "password": password,
                "returnSecureToken": True
            }
            
            response = requests.post(auth_url, json=payload)
            
            if response.status_code != 200:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message", "Login failed")
                raise RuntimeError(f"Authentication failed: {error_message}")
            
            auth_data = response.json()
            user_id = auth_data.get("localId")
            id_token = auth_data.get("idToken")
            refresh_token = auth_data.get("refreshToken")
            
            user_doc = self.db.collection(self.collection).document(user_id).get()
            
            if not user_doc.exists:
                raise RuntimeError("User data not found in database")
            
            user_data = user_doc.to_dict()
            
            custom_claims = {
                "personId": user_id,
                "firstName": user_data.get("first_name"),
                "lastName": user_data.get("last_name"),
                "email": user_data.get("email")
            }
            
            custom_token = firebase_auth.create_custom_token(user_id, custom_claims)
            
            return {
                "access_token": id_token,
                "refresh_token": refresh_token,
                "custom_token": custom_token.decode('utf-8'),
                "user_id": user_id,
                "user_data": {
                    "first_name": user_data.get("first_name"),
                    "last_name": user_data.get("last_name"),
                    "email": user_data.get("email")
                }
            }
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error during login: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Login failed: {str(e)}")

    def refresh_token(self, refresh_token: str):
        try:
            refresh_url = f"https://securetoken.googleapis.com/v1/token?key={self.firebase_api_key}"
            
            payload = {
                "grant_type": "refresh_token",
                "refresh_token": refresh_token
            }
            
            response = requests.post(refresh_url, json=payload)
            
            if response.status_code != 200:
                error_data = response.json()
                error_message = error_data.get("error", {}).get("message", "Token refresh failed")
                raise RuntimeError(f"Token refresh failed: {error_message}")
            
            token_data = response.json()
            
            return {
                "access_token": token_data.get("access_token"),
                "refresh_token": token_data.get("refresh_token"),
                "expires_in": token_data.get("expires_in")
            }
            
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error during token refresh: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Token refresh failed: {str(e)}")

    def verify_token(self, id_token: str):
        try:
            decoded_token = firebase_auth.verify_id_token(id_token)
            return decoded_token
        except firebase_auth.InvalidIdTokenError:
            raise RuntimeError("Invalid ID token")
        except firebase_auth.ExpiredIdTokenError:
            raise RuntimeError("Token has expired")
        except Exception as e:
            raise RuntimeError(f"Token verification failed: {str(e)}")

    def get_user_by_id(self, user_id: str):
        try:
            user_doc = self.db.collection(self.collection).document(user_id).get()
            
            if not user_doc.exists:
                raise RuntimeError("User not found")
            
            return user_doc.to_dict()
            
        except Exception as e:
            raise RuntimeError(f"Failed to get user data: {str(e)}")

    def logout_user(self, user_id: str):
        try:
            firebase_auth.revoke_refresh_tokens(user_id)
            return {"message": "User logged out successfully"}
        except Exception as e:
            raise RuntimeError(f"Logout failed: {str(e)}")