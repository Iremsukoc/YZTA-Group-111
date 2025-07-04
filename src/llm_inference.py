import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()  # .env dosyasından anahtarı al

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-1.5-pro")

def get_llm_response(label):
    prompt = f"Aşağıdaki sınıf tıbbi bir görüntüden elde edilmiştir: {label}. Bu sınıfın ne anlama geldiğini basitçe açıklar mısın?"
    
    response = model.generate_content(prompt)
    return response.text
