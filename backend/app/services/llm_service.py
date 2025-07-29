import os
import json
import re
from datetime import datetime
from dotenv import load_dotenv
import google.generativeai as genai

from app.prompts.assessment_prompts import TRIAGE_PROMPT, DETAILED_QA_SYSTEM_PROMPT
from app.prompts.general_test_chat_llm_prompt import general_test_chat_llm_prompt

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SAFE_DEFAULT = {
    "response": "Sorry, I couldn't parse that. Can you describe your main symptoms?",
    "next_step": "triage_in_progress"
}

def _extract_json(text: str) -> dict:
    """
    Gemini bazen JSON dışında metin dönebilir. İlk geçerli JSON objesini ayıklar.
    """
    if not text:
        return SAFE_DEFAULT

    cleaned = text.strip().replace("```json", "").replace("```", "")

    try:
        return json.loads(cleaned)
    except Exception:
        pass

    try:
        m = re.search(r"\{[\s\S]*\}", cleaned)
        if m:
            return json.loads(m.group(0))
    except Exception:
        pass

    return SAFE_DEFAULT

def _normalize_llm_output(llm_out: dict) -> dict:
    """
    LLM çıkışını normalize eder.
    """
    out = dict(SAFE_DEFAULT)

    if isinstance(llm_out, dict):
        if isinstance(llm_out.get("response"), str):
            out["response"] = llm_out["response"]

        ns = llm_out.get("next_step")
        if ns in ["general_test_in_progress", "triage_in_progress", "start_detailed_qa", "request_image", "completed"]:
            out["next_step"] = ns

        if "cancer_type" in llm_out and isinstance(llm_out["cancer_type"], str):
            ct = llm_out["cancer_type"].lower().strip()
            if ct in ["brain", "skin", "breast"]:
                out["cancer_type"] = ct

    return out

def get_llm_response(assessment: dict) -> dict:
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
    history = assessment.get("conversation", [])
    status = assessment.get("status", "general_test_in_progress")

    history_str = json.dumps(history, indent=2, default=str)

    try:
        if status == "general_test_in_progress":
            prompt = general_test_chat_llm_prompt + "\n\n---\n\nConversation History:\n" + history_str
        elif status == "triage_in_progress":
            prompt = TRIAGE_PROMPT.format(history=history_str)
        elif status == "detailed_qa_in_progress":
            cancer_type = assessment.get("suspectedCancerType", "Unknown")
            prompt = DETAILED_QA_SYSTEM_PROMPT.format(cancer_type=cancer_type.upper()) + "\n\nConversation:\n" + history_str
        else:
            return {"response": "Assessment is not in a chat phase.", "next_step": status}

        response = model.generate_content(prompt)
        raw_text = response.text.strip() if hasattr(response, "text") else ""
        parsed = _extract_json(raw_text)
        return _normalize_llm_output(parsed)

    except Exception as e:
        print("LLM Status:", status)
        if 'prompt' in locals():
            print("LLM Prompt:\n", prompt)
        else:
            print("Prompt oluşturulamadı.")
        print("LLM Hatası:", e)
        return {"response": "LLM hatası oluştu", "next_step": "error"}

