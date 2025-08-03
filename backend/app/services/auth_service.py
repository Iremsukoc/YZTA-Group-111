from firebase_admin import auth as firebase_auth
from firebase_admin import firestore
from app.dto.auth.register_dto import RegisterDTO

class AuthService:
    def register_new_user(self, user_data: RegisterDTO):
        created_user = firebase_auth.create_user(
            email=user_data.email,
            password=user_data.password,
            display_name=f"{user_data.first_name} {user_data.last_name}"
        )
        
        db = firestore.client()
        user_info = {
            "first_name": user_data.first_name,
            "last_name": user_data.last_name,
            "email": user_data.email,
            "created_at": firestore.SERVER_TIMESTAMP
        }
        db.collection('users').document(created_user.uid).set(user_info)

        claims = {
            "personId": created_user.uid,
            "firstName": user_data.first_name,
            "lastName": user_data.last_name,
            "email": user_data.email
        }
        firebase_auth.set_custom_user_claims(created_user.uid, claims)

        return created_user
    
    def change_password(self, user_id: str, new_password: str):
        firebase_auth.update_user(user_id, password=new_password)
        return {"message": "Password updated successfully."}

    def delete_user_account(self, user_id: str):
        db = firestore.client()

        db.collection('users').document(user_id).delete()
        firebase_auth.delete_user(user_id)

        return {"message": "User account deleted successfully."}