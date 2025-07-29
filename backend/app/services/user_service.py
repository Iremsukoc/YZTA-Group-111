from firebase_admin import firestore
from app.dto.user.user_dto import UpdateUserProfileDTO

class UserService:
    def update_profile(self, user_id: str, profile_data: UpdateUserProfileDTO):
        db = firestore.client()
        user_ref = db.collection('users').document(user_id)

        update_data = profile_data.dict(exclude_unset=True)

        if not update_data:
            return {"message": "No fields to update."}

        user_ref.update(update_data)

        updated_doc = user_ref.get()
        return updated_doc.to_dict()