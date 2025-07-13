from firebase_admin import auth as firebase_auth
from firebase_admin import firestore
from dto.user_dto import CreateUserDTO

def register_new_user(user_data: CreateUserDTO):

    try:
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

    except Exception as e:
        raise e