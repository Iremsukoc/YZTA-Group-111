import os
import google.generativeai as genai
from dotenv import load_dotenv

# .env dosyasını proje kökünden yükle
env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path=env_path)

# Gemini API yapılandırması
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro")

def get_llm_response(label):
    prompt = f"Meme kanseri sınıflandırmasında '{label}' sınıfı ne anlama gelir? Sadece kısa tıbbi açıklama yap."

    try:
        response = model.generate_content(prompt)

        if hasattr(response, 'text'):
            return response.text.strip()
        elif hasattr(response, 'parts') and len(response.parts) > 0:
            return response.parts[0].text.strip()
        else:
            return ""
    except Exception as e:
        return ""