# Lung Kanseri Sınıflandırma Modeli

Bu klasör, akciğer (lung) kanseri teşhisi için geliştirilmiş bir derin öğrenme modelini ve tahmin scriptlerini içerir. Model, X-ray veya benzeri tıbbi görüntüler üzerinden aşağıdaki üç sınıfı ayırt eder:

- `Benign cases` (iyi huylu)
- `Malignant cases` (kötü huylu)
- `Normal cases` (sağlıklı)

---

## 🗂️ Klasör Yapısı
Lung/
├── lung_cancer_cnn.h5 # Eğitilmiş model dosyası
├── test_split_lung/ # Test görselleri
│ ├── Benign cases/
│ ├── Malignant cases/
│ └── Normal cases/
├── utils.py # Görsel işleme ve tahmin yardımcı fonksiyonları
├── predict.py # Modeli yükleyip tahmin yapan script
└── README.md # Açıklama dosyası

---

## 📦 Gerekli Kütüphaneler

Bu projeyi çalıştırmadan önce aşağıdaki kütüphanelerin kurulu olması gerekir:

```bash
pip install tensorflow pillow opencv-python numpy


1-Kullanım
Ortamı aktive et:
    conda activate cancer-classification-env
2-Klasöre gir:
    cd Lung
3-Tahmin yap:
    python predict.py


Fonksiyon Açıklamaları (utils.py)
preprocess_single_image(image_path, target_size=(128, 128), color_mode='grayscale')
Amaç:
Modelin beklentisine göre görseli işler (boyutlandırır, normalize eder, kanal ve batch boyutu ekler).

İşlem adımları:

Görseli açar (PIL ile)

grayscale modundaysa gri tonlamaya çevirir

Yeniden boyutlandırır (128x128)

NumPy array'e çevirip float32 tipine getirir

0–1 aralığında normalize eder (/255.0)

Gerekirse kanal boyutu ([..., 1]) ekler

Batch boyutu ([1, ...]) ekler

Çıktı:
Modelin tahmin yapabileceği biçimde görsel array’i

predict_uploaded_image(image_path, model, label_map=None, target_size=(128, 128), color_mode='grayscale')
Amaç:
Verilen görsel dosyasına model ile tahmin yaptırır.

İşlem adımları:

Yukarıdaki preprocess_single_image() fonksiyonu ile işleme yapar

model.predict(...) ile sınıf olasılıklarını alır

En yüksek olasılığa sahip sınıfı argmax ile bulur

label_map verilmişse index yerine etiket ismi döndürür

Çıktı:

str: Sınıf etiketi (örneğin: 'Malignant cases')

veya int: Sınıf index’i (etiket verilmemişse)


predict.py Açıklaması
Bu dosya şu adımları yapar:

Model dosyasını (lung_cancer_cnn.h5) yükler

Test için örnek bir görseli belirler (örneğin: Normal cases/colorjitter (12).jpg)

utils.py içindeki fonksiyonlarla görüntüyü işler

Tahmin yapar ve sonucu ekrana yazdırır

⚠️ Notlar
IMAGE_PATH satırında kullanılan örnek görselin gerçekten var olduğuna emin olun.

Modeliniz farklı boyutlarda eğitildiyse target_size parametresini ona göre değiştirin.

color_mode yanlış verilirse model giriş boyutuyla uyumsuzluk hatası alırsınız.
