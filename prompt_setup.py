# gemini_config.py

import os
from dotenv import load_dotenv
import google.generativeai as genai
from pathlib import Path
from dotenv import load_dotenv

# .env dosyasını yükle
env_path = Path(__file__).resolve().parent.parent / ".env"

load_dotenv(dotenv_path=env_path)

# Ortam değişkeninden API anahtarını al
API_KEY = os.getenv("API_KEY") 

if API_KEY is None:
    raise ValueError("API_KEY bulunamadı. .env dosyanı kontrol et.")

# Google Gemini API'yi yapılandır
genai.configure(api_key=API_KEY)

# Model örneği (1.5 Pro kullanılıyor)
gemini_model = genai.GenerativeModel("gemini-1.5-pro")