import firebase_admin
from firebase_admin import credentials, firestore
from .config import FIREBASE_CREDENTIALS_PATH

db = None

def initialize_firebase_app():
    global db
    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK successfully initialized.")
        
        db = firestore.client()
        
    except Exception as e:
        raise RuntimeError(f"FATAL: Firebase Admin SDK initialization failed: {e}")
