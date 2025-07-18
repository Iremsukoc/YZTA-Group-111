import uuid
import google.generativeai as genai
from google.cloud import firestore
from app.services.firebase_service import FirebaseService
from app.prompts.general_test_chat_llm_prompt import general_test_chat_llm_prompt
from app.config.gemini_config import GEMINI_API_KEY


class GeneralTestChatService:
    COLLECTION_NAME = "GeneralTestChatHistory"

    def __init__(self):
        self.db = FirebaseService.get_db()
        
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel("gemini-1.5-pro")

    def start_new_chat(self, user_id: str) -> str:
        """Yeni chat oturumu başlat"""
        session_id = str(uuid.uuid4())
        doc_ref = (
            self.db.collection(self.COLLECTION_NAME)
            .document(user_id)
            .collection("sessions")
            .document(session_id)
        )

        from datetime import datetime
        doc_ref.set({
            "history": [{
                "role": "system",
                "content": general_test_chat_llm_prompt,
                "timestamp": datetime.now()
            }]
        })

        return session_id

    def get_chat_history(self, user_id: str, session_id: str) -> list:
        doc_ref = (
            self.db.collection(self.COLLECTION_NAME)
            .document(user_id)
            .collection("sessions")
            .document(session_id)
        )
        doc = doc_ref.get()
        
        if doc.exists:
            data = doc.to_dict()
            return data.get("history", [])
        return []

    def send_message(self, user_id: str, session_id: str, message: str) -> str:
        doc_ref = (
            self.db.collection(self.COLLECTION_NAME)
            .document(user_id)
            .collection("sessions")
            .document(session_id)
        )
        
        doc = doc_ref.get()
        if not doc.exists:
            raise RuntimeError("Chat session not found. Please start a new chat.")

        data = doc.to_dict()
        history = data.get("history", [])

        from datetime import datetime
        history.append({
            "role": "user",
            "content": message,
            "timestamp": datetime.now()
        })

        messages = [msg["content"] for msg in history if msg["role"] != "system"]

        try:
            response = self.model.generate_content(messages)
            response_text = response.text
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")

        history.append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now()
        })

        doc_ref.update({"history": history})

        return response_text