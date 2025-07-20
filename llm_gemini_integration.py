import sys
import os
import random
from pathlib import Path
from PIL import Image
from predict_system import CancerPredictor
import requests
import json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Gemini API integration ---
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro-latest:generateContent"
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set your API key as an environment variable

CANCER_TYPE_TO_TEST_POOL = {
    'skin': 'test_data_pool/skin',
    'breast': 'test_data_pool/breast',
    'brain': 'test_data_pool/brain',
}

def get_class_folders(cancer_type):
    if cancer_type == 'skin':
        return ['Benign', 'Malignant']
    elif cancer_type == 'breast':
        return ['benign', 'malignant', 'normal']
    elif cancer_type == 'brain':
        return ['glioma', 'meningioma', 'notumor', 'pituitary']
    else:
        return []

def select_random_image(cancer_type):
    test_pool = Path(CANCER_TYPE_TO_TEST_POOL[cancer_type])
    class_folders = get_class_folders(cancer_type)
    all_images = []
    for class_folder in class_folders:
        folder = test_pool / class_folder
        if folder.exists():
            for img_file in folder.glob('*'):
                if img_file.suffix.lower() in ['.png', '.jpg', '.jpeg']:
                    all_images.append(str(img_file))
    if not all_images:
        raise FileNotFoundError(f"No images found for {cancer_type} in {test_pool}")
    return random.choice(all_images)

def ask_gemini(prompt, api_key=None):
    if api_key is None:
        api_key = GEMINI_API_KEY
    if not api_key:
        raise ValueError("Gemini API key is not set. Set GEMINI_API_KEY environment variable or pass as argument.")
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 64}
    }
    response = requests.post(
        f"{GEMINI_API_URL}?key={api_key}",
        headers=headers,
        data=json.dumps(data)
    )
    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.status_code} {response.text}")
    result = response.json()
    # Extract the text response
    try:
        text = result['candidates'][0]['content']['parts'][0]['text']
        return text.strip()
    except Exception:
        return str(result)

def build_gemini_prompt(user_symptoms):
    return (
        "You are a medical expert specializing only in skin, breast, and brain cancers. "
        "Given the user's symptoms, respond with only one word: either 'skin', 'breast', or 'brain' — whichever cancer type is most likely. "
        "Do not provide any explanation, translation, or extra information. "
        "Only output the most likely cancer type as a single word.\n"
        f"User symptoms: {user_symptoms}"
    )

def extract_cancer_type_from_llm_response(llm_response):
    llm_response = llm_response.lower()
    if 'skin' in llm_response or 'deri' in llm_response:
        return 'skin'
    elif 'breast' in llm_response or 'meme' in llm_response:
        return 'breast'
    elif 'brain' in llm_response or 'beyin' in llm_response:
        return 'brain'
    # fallback: ilk kelimeyi dene
    first_word = llm_response.split()[0]
    if first_word in ['skin', 'deri']:
        return 'skin'
    elif first_word in ['breast', 'meme']:
        return 'breast'
    elif first_word in ['brain', 'beyin']:
        return 'brain'
    raise ValueError(f"Could not extract cancer type from LLM response: {llm_response}")

def llm_gemini_inference(user_prompt, api_key=None):
    print(f"Kullanıcı: {user_prompt}")
    # 1. LLM'den tanı al
    llm_response = ask_gemini(user_prompt, api_key=api_key)
    print(f"Gemini LLM: {llm_response}")
    # 2. Tanıdan kanser türünü çıkar
    cancer_type = extract_cancer_type_from_llm_response(llm_response)
    print(f"[Sistem] Tespit edilen kanser türü: {cancer_type}")
    print(f"[Sistem] Lütfen {cancer_type} bölgesinin tıbbi görüntüsünü yükleyin.")
    # 3. Görsel yüklemesini simüle et (rastgele görsel seç)
    image_path = select_random_image(cancer_type)
    print(f"[Simülasyon] Kullanıcıdan alınan görüntü: {image_path}")
    # Show the image to the user
    try:
        img = Image.open(image_path)
        img.show()
    except Exception as e:
        print(f"Görsel gösterilemedi: {e}")
    # 4. Model tahmini
    predictor = CancerPredictor()
    result = predictor.predict_single_image(image_path, cancer_type)
    print(f"\nModel Tahmini:")
    print(f"Görsel: {image_path}")
    print(f"Tahmin edilen sınıf: {result.get('predicted_class', 'Error')}")
    print(f"Güven skoru: {result.get('confidence', 0)}%")
    return result

if __name__ == "__main__":
    # API key'i doğrudan burada da verebilirsin veya ortam değişkeni olarak ayarlayabilirsin
    # os.environ['GEMINI_API_KEY'] = 'YOUR_API_KEY_HERE'
    user_symptoms = input("Semptomunuzu girin: ")
    prompt = build_gemini_prompt(user_symptoms)
    llm_response = ask_gemini(prompt)
    llm_gemini_inference(llm_response) 