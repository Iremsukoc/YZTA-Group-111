# Kanser Tespit Sistemi: Backend ve Frontend Entegrasyonu

Bu proje, çeşitli kanser türlerinin (beyin, meme, cilt, kolon, lösemi, akciğer) görüntü tabanlı tespiti için derin öğrenme modelleri içeren bir backend ve buna bağlanabilen bir frontend arayüzü geliştirmeyi amaçlar.

## İçerik
- [Gereksinimler](#gereksinimler)
- [Kurulum](#kurulum)
- [Backend Çalıştırma](#backend-calistirma)
- [Frontend ile Entegrasyon](#frontend-ile-entegrasyon)
- [API Kullanımı](#api-kullanimi)
- [Notlar](#notlar)

---

## Gereksinimler
- Python 3.8+
- CUDA destekli GPU ve uygun CUDA sürücüleri (GPU ile çalışmak için)
- pip
- (Varsa) Frontend için Node.js ve npm/yarn

### Python Kütüphaneleri
Backend için gerekli kütüphaneler `requirements.txt` dosyalarında belirtilmiştir. Ana kütüphaneler:
- torch (PyTorch)
- torchvision
- numpy
- pillow
- matplotlib
- pyyaml

## Kurulum
1. **Depoyu klonlayın:**
   ```bash
   git clone <proje-linki>
   cd documention
   ```
2. **Gerekli Python kütüphanelerini yükleyin:**
   ```bash
   pip install -r bootcamp/bootcamp/colon-cancer-detector/requirements.txt
   pip install -r bootcamp/bootcamp/leukemia-classifier/requirements.txt
   pip install -r bootcamp/bootcamp/lung_cancer_project/requirements.txt
   # Ana dizinde ek olarak
   pip install torch torchvision numpy pillow matplotlib pyyaml
   ```
3. **CUDA kurulumu:**
   - CUDA ve cuDNN sürücülerinizin yüklü olduğundan emin olun.
   - PyTorch'un CUDA destekli sürümünü yükleyin: https://pytorch.org/get-started/locally/

## Backend Çalıştırma
Backend, Python tabanlıdır ve REST API olarak sunulabilir. Önerilen yol FastAPI veya Flask ile bir API servisi oluşturmaktır.

### Örnek FastAPI Sunucusu
1. **FastAPI ve Uvicorn yükleyin:**
   ```bash
   pip install fastapi uvicorn
   ```
2. **Basit bir API dosyası oluşturun (ör: `api_server.py`):**
   ```python
   from fastapi import FastAPI, UploadFile, File, Form
   from predict_system import CancerPredictor
   import shutil
   import os

   app = FastAPI()
   predictor = CancerPredictor(device='cuda')

   @app.post("/predict/")
   async def predict(cancer_type: str = Form(...), file: UploadFile = File(...)):
       temp_path = f"temp_{file.filename}"
       with open(temp_path, "wb") as buffer:
           shutil.copyfileobj(file.file, buffer)
       result = predictor.predict_single_image(temp_path, cancer_type)
       os.remove(temp_path)
       return result
   ```
3. **API'yi başlatın:**
   ```bash
   uvicorn api_server:app --reload
   ```
   - API varsayılan olarak `http://127.0.0.1:8000` adresinde çalışır.
   - `/docs` adresinden Swagger arayüzü ile test edebilirsiniz.

## Frontend ile Entegrasyon
Frontend, React, Vue, Angular veya başka bir framework ile geliştirilebilir. Temel olarak, kullanıcıdan resim ve kanser türü alıp, backend'e POST isteği gönderir.

### Örnek İstek (JavaScript/React):
```js
const formData = new FormData();
formData.append('cancer_type', 'skin');
formData.append('file', selectedFile);

fetch('http://127.0.0.1:8000/predict/', {
  method: 'POST',
  body: formData
})
  .then(res => res.json())
  .then(data => console.log(data));
```
- `selectedFile` kullanıcının yüklediği dosyadır.
- `cancer_type` değerleri: `brain`, `breast`, `skin` (gerekirse diğerleri eklenebilir)

## API Kullanımı
- **Endpoint:** `/predict/`
- **Yöntem:** `POST`
- **Parametreler:**
  - `cancer_type`: (string) Kanser türü (`brain`, `breast`, `skin` ...)
  - `file`: (image) Yüklenecek resim dosyası
- **Dönüş:**
  - Tahmin edilen sınıf, güven skoru ve varsa olasılıklar

## Notlar
- Model dosyalarının ve test görsellerinin doğru dizinlerde olduğundan emin olun.
- GPU kullanılacaksa CUDA sürücülerinizin ve PyTorch CUDA sürümünün uyumlu olması gerekir.
- Geliştirme ve test için backend'i önce başlatın, ardından frontend'den istek gönderin.
- Gerekirse API endpointlerini frontend projesinde `.env` dosyası ile yönetebilirsiniz.

---

Herhangi bir sorunda veya geliştirme ihtiyacında proje yöneticisine veya geliştirici ekibe ulaşabilirsiniz. 