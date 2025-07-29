# Kanser Tespit Sistemi

Bu proje, çeşitli kanser türlerinin (beyin, meme, cilt) görüntü tabanlı tespiti için derin öğrenme modelleri içeren bir sistemdir.

## Proje Yapısı

### Ana Bileşenler

#### `predict_system.py` - Ana Tahmin Sistemi
- **Görevi**: Tüm kanser türleri için tek bir arayüz sağlar
- **Özellikler**:
  - 3 farklı kanser türü için model yükleme (brain, breast, skin)
  - GPU/CPU desteği
  - Tek resim ve batch tahmin
  - Otomatik transform uygulama

#### Kanser Türleri ve Modeller

**1. Beyin Tümörü (Brain Tumor)**
- **Model**: `brain_tumor/saved_model.pth`
- **Sınıflar**: glioma, meningioma, notumor, pituitary
- **Transform**: 224x224 resize, ImageNet normalization
- **Utils**: `brain_tumor/utils.py`

**2. Meme Kanseri (Breast Cancer)**
- **Model**: `breast_cancer/breast_cancer_model.pth`
- **Sınıflar**: benign, malignant, normal
- **Transform**: 224x224 resize, RGB conversion, [-0.5, 0.5] normalization
- **Utils**: `breast_cancer/utils.py`

**3. Cilt Kanseri (Skin Cancer)**
- **Model**: `skin_cancer/best_model.pth`
- **Sınıflar**: Benign, Malignant (binary classification)
- **Transform**: 112x112 resize, ImageNet normalization
- **Utils**: `skin_cancer/src/preprocessing.py`

### Test Veri Havuzu

#### `test_data_pool/` - Test Veri Setleri 
Her kanser türü için ayrı test verileri:
```
test_data_pool/
├── brain/
│   ├── glioma/
│   ├── meningioma/
│   ├── notumor/
│   └── pituitary/
├── breast/
│   ├── benign/
│   ├── malignant/
│   └── normal/
└── skin/
    ├── Benign/
    └── Malignant/
```

Veri setini indirin: [test_data_pool](https://drive.google.com/drive/folders/1MWCyP-nj-gzxZYCW2IXNa7OOFbv7t3Yf)

### Transform İşlemleri

Her kanser türü için özel transform'lar uygulanır:

**Brain Tumor:**
```python
transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
```

**Breast Cancer:**
```python
transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.Lambda(lambda img: img.convert("RGB")),  # Grayscale to RGB
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
])
```

**Skin Cancer:**
```python
transforms.Compose([
    transforms.Resize((112, 112)),
    transforms.CenterCrop((112, 112)),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
])
```

## Kullanım

### Tek Resim Tahmini
```python
predictor = CancerPredictor(device='cuda')
result = predictor.predict_single_image('image.jpg', 'brain')
print(f"Tahmin: {result['predicted_class']}, Güven: {result['confidence']}%")
```

### Batch Tahmin
```python
results = predictor.batch_predict('skin', num_images=5)
for result in results:
    print(f"{result['image_path']} → {result['predicted_class']}")
```

### Test Veri Havuzundan Rastgele Örnekler
```python
test_images = predictor.get_random_test_images('breast', num_images=3)
```

## Gereksinimler

### Python Kütüphaneleri
```bash
pip install torch torchvision numpy pillow matplotlib pyyaml
```

### GPU Desteği
CUDA destekli GPU için:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

## Model Dosyaları

Her model için gerekli dosyalar:
- **Brain**: `brain_tumor/saved_model.pth`
- **Breast**: `breast_cancer/breast_cancer_model.pth`
- **Skin**: `skin_cancer/best_model.pth`


Model dosyalarını indirin: [Model dosyaları](https://drive.google.com/drive/folders/1q1Mh068hp4trI5pDPolN6GOBJYL4qqs7)

## Notlar

- Modeller GPU'da çalışmak üzere optimize edilmiştir
- Test verileri `test_data_pool/` klasöründe organize edilmiştir
- Her kanser türü için özel transform'lar uygulanır
- Binary (skin) ve multi-class (brain, breast) sınıflandırma desteklenir

---

Bu sistem, farklı kanser türleri için tutarlı bir tahmin arayüzü sağlar ve her model için optimize edilmiş transform'lar kullanır. 
