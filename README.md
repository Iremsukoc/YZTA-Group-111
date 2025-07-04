# 🩺 Breast Cancer Classification using ResNet101

Bu proje, **BUSI with GT** ultrason görüntüleri veri seti kullanılarak, meme kanseri sınıflandırması yapmayı amaçlamaktadır. Eğitimde **ResNet101** mimarisi kullanılmış ve modelin başarımı hem doğruluk hem de F1 skorları ile değerlendirilmiştir.

---

## 📁 Proje Yapısı

```
breast_cancer_project_pytorch/
├── data/
│   ├── breast_cancer_dataset/              # Orijinal veri seti (BUSI)
│   └── breast_cancer_dataset_split/        # Eğitim/Doğrulama/Test ayrımı yapılmış veri
├── saved_model/
│   └── best_model.pth                      # En iyi doğrulukla kaydedilen model
├── src/
│   ├── config.py                           # Hiperparametreler ve ayarlar
│   ├── data_utils.py                       # Dataloader fonksiyonu
│   ├── model.py                            # Model tanımı (ResNet101)
│   ├── train.py                            # Eğitim scripti
│   ├── predict_single_image.py            # Tek bir görsel tahmini
│   └── llm_inference.py                    # (Opsiyonel) LLM ile sonuç yorumu
├── .env                                    # Ortam değişkenleri (Git'e dahil edilmez)
├── .gitignore                              # Takip edilmeyecek dosya ve klasörler
└── requirements.txt                        # Gerekli Python paketleri
```

---

## 🚀 Kurulum

### 1. Ortamı Kurun

```bash
git clone https://github.com/Iremsukoc/YZTA-Bootcamp.git
cd YZTA-Bootcamp
git checkout -b ml-1.0.2/image-classification-core
cd breast_cancer_project_pytorch
```


### 2. Sanal Ortam ve Gereksinimler

```bash
conda create -n breast_cancer python=3.10 -y
conda activate breast_cancer
pip install -r requirements.txt
```

---

## 🧠 Model Bilgisi

Model: **ResNet101**  
Kayıp fonksiyonu: CrossEntropyLoss  
Optimizasyon: Adam  
Epoch: 10  
En iyi model `.pth` dosyası olarak `saved_model/best_model.pth` altında saklanır.

---

## 📊 Sonuçlar

### ✅ Eğitim Sonuçları

- Train Accuracy: **99.37%**
- Validation Accuracy: **96.17%**

### 📉 Classification Report

| Sınıf     | Precision | Recall | F1-Score | Support |
|-----------|-----------|--------|----------|---------|
| benign    | 0.91      | 0.87   | 0.89     | 135     |
| malignant | 0.86      | 0.78   | 0.82     | 64      |
| normal    | 0.75      | 0.95   | 0.84     | 41      |
| **Accuracy** |       |        | **0.86** | 240     |

### 📌 Confusion Matrix

```
[[118   7  10]
 [ 11  50   3]
 [  1   1  39]]
```

---

## 🧪 Modeli Test Etme

Aşağıdaki komut ile test verisinden rastgele bir örnek üzerinde tahmin yapabilirsiniz:

```bash
python src/predict_single_image.py
```

---

## 📌 Notlar

- Model eğitimi sırasında en iyi doğruluk elde edilen model `saved_model/` altında saklanır.
- `config.py` dosyasındaki parametreleri değiştirerek eğitim ayarlarını özelleştirebilirsiniz.
- `llm_inference.py` modülü, çıktıyı doğal dilde yorumlama için örnek olarak sunulmuştur.

---
