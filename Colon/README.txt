# Colon Kanseri Sınıflandırma Modeli

Bu klasör, kolon kanseri görüntülerini sınıflandırmak için eğitilmiş bir derin öğrenme modelini ve tahmin scriptlerini içerir. Model, iki sınıf arasında ayrım yapar:

- `Colon_adenocarcinoma`
- `Colon_benign_tissue`

## 🔧 Dosya Yapısı
Colon/
├── model_cnn.h5 # Eğitilmiş Keras modeli
├── test_split_colon/ # Test görsellerinin bulunduğu klasör
│ ├── Colon_adenocarcinoma/
│ └── Colon_benign_tissue/
├── utils.py # Görüntü işleme ve tahmin fonksiyonları
├── predict.py # Modeli kullanarak görsel sınıflandırma yapan script
└── README.md # Açıklama dosyası (bu dosya)


## 📦 Gerekli Kütüphaneler

- TensorFlow
- Pillow (görsel işleme)
- NumPy

Sanal ortam (Anaconda) kullanılması önerilir.

```bash
conda create --name cancer-ai-env python=3.10
conda activate cancer-ai-env
pip install tensorflow pillow numpy

Kullanım
1-Ortamı aktif hale getir:
    conda activate cancer-ai-env
2-Klasöre git:
    cd Colon
3-Tahmin yapmak için script'i çalıştır:
    python predict.py

Script Açıklamaları
utils.py:
Görselleri modele uygun hale getirmek (yeniden boyutlandırma, normalize etme vb.) ve tahmin işlemleri için yardımcı fonksiyonları içerir.

predict.py:

Modeli yükler (model_cnn.h5)

Test görselini işler (test_split_colon/...)

Tahmin yapar ve sonucu ekrana yazdırır

Notlar
Test için örnek görsel yolu predict.py içinde sabit olarak verilmiştir. Farklı bir görsel test etmek istersen image_path satırını değiştirmen yeterlidir.

Klasör isimleri ve model adı farklıysa predict.py içinde güncelleme yapman gerekir.

Fonksiyon Açıklamaları (utils.py)
1. transform_image(uploaded_image, target_size=(224, 224))
Amaç:
Yüklenen bir görseli derin öğrenme modeline uygun hale getirir.

İşlem adımları:

Görseli RGB formatına dönüştürür (siyah-beyaz vs. karışmasın diye).

Belirtilen boyuta (224x224) yeniden boyutlandırır (modelin giriş boyutu).

Görseli NumPy array’e çevirir.

Piksel değerlerini 0-1 aralığına normalize eder (/255.0).

Ekstra bir boyut ekler (batch dimension: [1, 224, 224, 3])

Kullanıldığı yer:
predict.py içinde test görseli bu fonksiyonla işlenir.

2. predict_image(model, img_array, class_names)
Amaç:
İşlenmiş bir görsel üzerinden tahmin yapar.

İşlem adımları:

model.predict(...) ile sınıf olasılıklarını alır.

En yüksek olasılığa sahip sınıfın index’ini bulur (np.argmax()).

Index’e karşılık gelen sınıf adını class_names listesinden çeker.

O sınıfa ait olasılığı da güven oranı (confidence) olarak verir.

Döndürdüğü:

Tahmin edilen sınıf etiketi (string)

Güven oranı (float)

Kullanıldığı yer:
predict.py içinde model tahmini bu fonksiyonla yapılır.