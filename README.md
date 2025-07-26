
# Kanser Sınıflandırma API'si (Colon, Akciğer, Lösemi)

- Bu proje, yüklenen bir görüntüye göre kolon kanseri, akciğer kanseri ve lösemi sınıflandırması yapan bir FastAPI tabanlı servistir. Modellerin hepsini bir arada veya tek tek çalıştırma imkanı vardır.

- Proje içerisinde yer alan Lösemi modeli model boyutu sebebiyle githuba yüklenememektedir. Manuel olarak indirip Models_Services/LeukemiaProject/ içerisine konması gerekmektedir. 

- Uygulamayı çalıştırdıktan sonra /test_images klasöründe yer alan görüntüleri kullanarak test yapılabilir.

- Leukemia Modeli : [indir](https://drive.google.com/file/d/12Vjt6pj3pI-jgg8dO1UMNFRE-BR-qTNF/view?usp=drive_link)

## Özellikler

- Üç farklı model:
  - Colon kanseri (CNN)
  - Akciğer kanseri (CNN)
  - Lösemi (ResNet50)
- FastAPI ile REST API arayüzü
- Swagger arayüzü üzerinden test imkânı
- `image/jpeg` ve `image/png` destekli

---

## Proje Yapısı

```
Models_Services/
│
├── main.py
├── ColonProject/
│   ├── colon_service.py
│   └── utils.py
│
├── LungProject/
│   ├── lung_service.py
│   └── utils.py
│
├── LeukemiaProject/
│   ├── leukemia_service.py
│   └── utils.py
```

---

## Gereksinimler

```bash
pip install -r requirements.txt
```

> Gerekli kütüphaneler: `fastapi`, `uvicorn`, `tensorflow`, `numpy`, `Pillow`

---

## Uygulamayı Başlat

```bash
python -m uvicorn main:app --reload --port 8080
```


veya


```bash
uvicorn main:app --reload --port 8080
```

> `--port` parametresi ile çalıştırmak istediğin portu belirleyebilirsin.

---

## Test Etme (Swagger UI)

Uygulama çalıştıktan sonra [http://127.0.0.1:8080/docs](http://127.0.0.1:8080/docs) adresine giderek görsel yükleyip tahminleri test edebilirsin.

---

## API Uç Noktaları

### Colon Kanseri Tahmini

```
POST /predict/colon
```

### Akciğer Kanseri Tahmini

```
POST /predict/lung
```

### Lösemi Tahmini

```
POST /predict/leukemia
```

Her endpoint `multipart/form-data` tipinde bir `file` alır ve şu şekilde yanıt döner:

```json
{
  "prediction": "Tahmin Edilen Sınıf"
}
```

---

## Notlar

- Tüm modeller `.h5` formatındadır ve proje içindeki ilgili klasörlerde yer almalıdır.
- Sadece `.jpeg` ve `.png` uzantılı görseller desteklenmektedir.
