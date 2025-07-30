import uuid
import os
from datetime import datetime, timezone
from fastapi import UploadFile
from firebase_admin import firestore
from app.services import llm_service
from ml_engine.predict_system import CancerPredictor
import numpy as np

def convert_numpy(obj):
    if isinstance(obj, dict):
        return {k: convert_numpy(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [convert_numpy(v) for v in obj]
    elif isinstance(obj, (np.float32, np.float64)):
        return float(obj)
    elif isinstance(obj, (np.int32, np.int64)):
        return int(obj)
    else:
        return obj


class AssessmentService:
    def __init__(self):
        self.predictor = CancerPredictor()

    def create_assessment_session(self, user_id: str, assessment_type: str) -> str:
        db = firestore.client()
        new_assessment_id = str(uuid.uuid4())
        assessment_ref = db.collection('assessments').document(new_assessment_id)

        user_assessments = db.collection('assessments') \
            .where('userId', '==', user_id) \
            .where('assessmentType', '==', assessment_type) \
            .stream()
        count = len(list(user_assessments))
        formatted_type = assessment_type.replace('_', ' ').title()
        display_name = f"{formatted_type} {count + 1}"

        assessment_data = {
            "userId": user_id,
            "assessmentType": assessment_type,
            "assessmentName": display_name,
            "createdAt": firestore.SERVER_TIMESTAMP,
            "updatedAt": firestore.SERVER_TIMESTAMP,
            "status": "general_test_in_progress",
            "suspectedCancerType": None,
            "finalRiskScore": None,
            "finalReport": None,
            "conversation": [],
            "imageAnalysisResult": None,
        }

        assessment_ref.set(assessment_data)
        return new_assessment_id

    def add_message_to_assessment(self, assessment_id: str, user_id: str, message_content: str) -> dict:
        db = firestore.client()
        assessment_ref = db.collection('assessments').document(assessment_id)
        doc = assessment_ref.get()

        if not doc.exists or doc.to_dict().get('userId') != user_id:
            raise PermissionError("User is not authorized to access this assessment.")

        data = doc.to_dict()
        conversation = data.get("conversation", [])
        now = datetime.now(timezone.utc)

        user_message = {"role": "user", "content": message_content, "timestamp": now}
        conversation.append(user_message)
        data["conversation"] = conversation

        llm_output = llm_service.get_llm_response(data)
        response_text = llm_output.get("response")
        next_step = llm_output.get("next_step")

        # Create a regular assistant message (not a diagnosis message)
        assistant_message = {
            "role": "assistant",
            "content": response_text,
            "timestamp": now
        }
        update_data = {
            "conversation": firestore.ArrayUnion([user_message, assistant_message]),
            "updatedAt": firestore.SERVER_TIMESTAMP
        }

        if llm_output.get("cancer_type"):
            data["suspectedCancerType"] = llm_output["cancer_type"]
            current_name = data.get("assessmentName") or ""
            new_type = llm_output["cancer_type"]
            if current_name.lower().startswith("general test"):
                assessments = db.collection("assessments") \
                    .where("userId", "==", user_id) \
                    .stream()
                count = 1
                for a in assessments:
                    existing_name = a.to_dict().get("assessmentName", "").lower()
                    if new_type.replace('_', ' ') in existing_name:
                        count += 1
                new_name = f"{new_type.replace('_', ' ').title()} Test {count}"
                update_data["assessmentName"] = new_name    

        current_status = data.get("status")

        if current_status == "general_test_in_progress" and next_step == "triage_in_progress":
            update_data["status"] = "triage_in_progress"
        elif next_step == "start_detailed_qa":
            update_data["status"] = "detailed_qa_in_progress"
            update_data["suspectedCancerType"] = llm_output.get("cancer_type")
        elif next_step == "request_image":
            update_data["status"] = "awaiting_image"
            if llm_output.get("cancer_type"):
                update_data["suspectedCancerType"] = llm_output.get("cancer_type")


        print("UPDATE DATA SENT TO FIRESTORE:", update_data)
        assessment_ref.set(update_data, merge=True)
        return {"role": "assistant", "content": response_text, "new_status": update_data.get("status", current_status)}


    def get_assessment_messages(self, assessment_id: str, user_id: str) -> list[dict]:
        db = firestore.client()
        assessment_ref = db.collection('assessments').document(assessment_id)
        doc = assessment_ref.get()
        if not doc.exists or doc.to_dict().get('userId') != user_id:
            raise PermissionError("User is not authorized to access this assessment.")
        conversation = doc.to_dict().get("conversation", [])
        return [{"role": msg["role"], "content": msg["content"]} for msg in conversation]

    async def analyze_image(self, user_id, assessment_id, image_file, model_type=None):
        db = firestore.client()
        assessment_ref = db.collection('assessments').document(assessment_id)
        doc = assessment_ref.get()

        if not doc.exists or doc.to_dict().get('userId') != user_id:
            raise PermissionError("User is not authorized for this assessment.")
            
        data = doc.to_dict()
        valid_models = ['brain', 'skin', 'breast', 'colon', 'lung', 'leukemia']
        suspected = (data.get("suspectedCancerType") or "").lower().strip()
        assessment_type = (data.get("assessmentType") or "").lower().strip()
        if suspected in valid_models:
            selected = suspected
        elif assessment_type in valid_models:
            selected = assessment_type
        else:
            selected = "brain"

        if model_type and model_type.lower().strip() != selected:
            print(f"[WARN] Client-passed model_type '{model_type}' ignored. Using '{selected}' from DB.")

        model_type = selected

        temp_dir = "temp_uploads"
        os.makedirs(temp_dir, exist_ok=True)
        file_extension = os.path.splitext(image_file.filename)[1]
        temp_filename = f"{uuid.uuid4()}{file_extension}"
        file_path = os.path.join(temp_dir, temp_filename)

        try:
            with open(file_path, "wb") as buffer:
                content = await image_file.read()
                buffer.write(content)

            ml_result = self.predictor.predict_single_image(file_path, model_type)

            if "error" in ml_result:
                raise Exception(f"ML script returned an error: {ml_result['error']}")
            ml_result = convert_numpy(ml_result)

            print("ML_RESULT:", ml_result)

            for key, value in ml_result.items():
                if isinstance(value, np.generic):
                    ml_result[key] = float(value)
                elif isinstance(value, dict):
                    for sub_key, sub_value in value.items():
                        if isinstance(sub_value, np.generic):
                            ml_result[key][sub_key] = float(sub_value)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

        # Create diagnosis message with ML results
        now = datetime.now(timezone.utc)
        diagnosis_message = {
            "role": "assistant",
            "type": "diagnosis",
            "timestamp": now,
            "content": {
                "title": "Diagnosis Complete",
                "result": ml_result.get("predicted_class", "Unknown"),
                "confidence": ml_result.get("confidence"),
                "note": "This is not a final diagnosis. Please consult a medical professional."
            }
        }

        update_data = {
            "status": "completed",
            "imageAnalysisResult": ml_result,
            "usedModel": model_type,
            "conversation": firestore.ArrayUnion([diagnosis_message]),
            "updatedAt": firestore.SERVER_TIMESTAMP
        }
        assessment_ref.update(update_data)
        return ml_result

    def get_all_assessments(self, user_id: str, status: str = None) -> list[dict]:
        db = firestore.client()
        query = db.collection('assessments').where('userId', '==', user_id)
        if status:
            query = query.where('status', '==', status)
        docs = query.stream()
        results = []
        for doc in docs:
            data = doc.to_dict()
            created_at = data.get("createdAt")
            results.append({
                "assessment_id": doc.id,
                "user_id": user_id,
                "status": data.get("status", ""),
                "created_at": created_at.isoformat() if hasattr(created_at, "isoformat") else str(created_at),
                "assessment_type": data.get("assessmentType"),
                "assessment_name": data.get("assessmentName"),
                "risk_level": data.get("suspectedCancerType"),
                "confidence": None,
                "conversation": data.get("conversation", [])
            })
        return results

    def get_report_summaries(self, user_id: str) -> list[dict]:
        db = firestore.client()
        query = (
            db.collection('assessments')
            .where('userId', '==', user_id)
            .order_by('updatedAt', direction=firestore.Query.DESCENDING)
        )

        docs = query.stream()
        results = []

        def to_risk(conf):
            if conf is None:
                return None
            if conf >= 80:
                return "High Risk"
            elif conf >= 50:
                return "Medium Risk"
            return "Low Risk"

        for doc in docs:
            data = doc.to_dict()
            print(f"FINAL NAME SENT: {data.get('assessmentName')}")  # log
            print(f"DATA ID: {doc.id}")
            print(f"AssessmentName: {data.get('assessmentName')}")
            print(f"AssessmentType: {data.get('assessmentType')}")
            img_res = data.get('imageAnalysisResult') or {}
            predicted_class = img_res.get('predicted_class')
            confidence = img_res.get('confidence')

            created_at = data.get('createdAt')
            updated_at = data.get('updatedAt')

            results.append({
                "assessment_id": doc.id,
                "assessment_type": data.get('assessmentType', ''),
                "title": data.get("assessmentName") or data.get("assessmentType"),
                "status": data.get('status', ''),
                "created_at": created_at.isoformat() if hasattr(created_at, "isoformat") else str(created_at),
                "updated_at": updated_at.isoformat() if hasattr(updated_at, "isoformat") else str(updated_at),
                "predicted_class": predicted_class,
                "confidence": confidence,
                "risk_level": to_risk(confidence),
                "can_continue": data.get('status') != 'completed'
            })
        return results

    def get_assessment_detail(self, assessment_id: str, user_id: str) -> dict:
        db = firestore.client()
        assessment_ref = db.collection('assessments').document(assessment_id)
        doc = assessment_ref.get()
        
        if not doc.exists:
            raise Exception("Assessment not found.")

        data = doc.to_dict()
        if data.get("userId") != user_id:
            raise PermissionError("User is not authorized to access this assessment.")
        
        created_at = data.get("createdAt")
        image_result = data.get("imageAnalysisResult") or {}
        risk_level = image_result.get("predicted_class", "Unknown")
        confidence = image_result.get("confidence")

        return {
            "assessment_id": assessment_id,
            "user_id": user_id,
            "assessmentName": data.get("assessmentName"),
            "assessment_type": data.get("assessmentType"),
            "created_at": str(created_at) if created_at else None,
            "risk_level": risk_level,
            "confidence": confidence,
            "status": data.get("status"),
            "conversation": data.get("conversation", []),
        }

