import firebase_admin
from firebase_admin import credentials, firestore, auth
from .config import FIREBASE_CREDENTIALS_PATH

try:
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred)
    print("Firebase Admin SDK başarıyla başlatıldı.")
except Exception as e:
    print(f"Firebase Admin SDK başlatılırken hata oluştu: {e}")


db = firestore.client()
