import firebase_admin
from firebase_admin import auth, credentials, firestore
from app.config.firebase_config import FIREBASE_CREDENTIALS_PATH

class FirebaseService:
    _db = None

    @classmethod
    def initialize_firebase_app(cls):
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK successfully initialized.")
        cls._db = firestore.client()

    @classmethod
    def get_db(cls):
        if cls._db is None:
            cls.initialize_firebase_app()
        return cls._db

    @staticmethod
    def get_auth():
        if not firebase_admin._apps:
            FirebaseService.initialize_firebase_app()
        return auth
