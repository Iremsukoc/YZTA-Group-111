from firebase_admin import firestore
from firebase_admin import auth as firebase_auth
from app.dto.user.user_dto import UpdateUserProfileDTO

class UserService:
    def update_profile(self, user_id: str, profile_data: UpdateUserProfileDTO):
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)

        update_data = profile_data.dict(exclude_unset=True)

        if not update_data:
            return {"message": "No fields to update."}

        user_ref.update(update_data)

        # Update Firebase Auth custom claims if first_name or last_name is being updated
        if 'first_name' in update_data or 'last_name' in update_data:
            # Get the current user data to preserve existing fields
            current_user_data = user_ref.get().to_dict()
            
            # Update custom claims
            claims = {
                "personId": user_id,
                "firstName": current_user_data.get('first_name', ''),
                "lastName": current_user_data.get('last_name', ''),
                "email": current_user_data.get('email', '')
            }
            firebase_auth.set_custom_user_claims(user_id, claims)

        updated_doc = user_ref.get()
        return updated_doc.to_dict()