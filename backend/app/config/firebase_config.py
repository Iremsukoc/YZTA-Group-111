# app/core/config.py
import os
import sys
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials

load_dotenv()

FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH")


def initialize_firebase_app():
    try:
        if not FIREBASE_CREDENTIALS_PATH:
            raise ValueError("FIREBASE_CREDENTIALS_PATH environment variable is not set.")
        
        if not firebase_admin._apps:
            cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK successfully initialized.", file=sys.stdout)
    
    except Exception as e:
                raise RuntimeError(f"FATAL: Firebase Admin SDK initialization failed: {e}")
