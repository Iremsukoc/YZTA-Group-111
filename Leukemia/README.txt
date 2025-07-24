# Lösemi Hücre Sınıflandırma Modeli

Bu klasör, mikroskop görüntüleri üzerinden lösemi (leukemia) hücrelerini sınıflandırmak için eğitilmiş bir derin öğrenme modelini içerir. Model, ResNet50 tabanlıdır ve 4 farklı hücre evresini tanıyabilir:

- `Benign`  → İyi huylu
- `Early`   → Erken evre
- `Pre`     → Ön evre
- `Pro`     → Proliferatif (ileri) evre

---

## 🗂️ Klasör Yapısı
Leukemia/
├── leukemia_resnet_model.h5 # Eğitilmiş model dosyası
├── test_split_leukemia/ # Test görselleri
│ ├── Benign/
│ ├── Early/
│ ├── Pre/
│ └── Pro/
├── utils.py # Görsel işleme ve tahmin yardımcıları
├── predict.py # Modeli çalıştırıp tahmin yapan script
└── README.md # Bu dokümantasyon dosyası


---

## 📦 Gerekli Kütüphaneler

Bu klasörü çalıştırmak için aşağıdaki kütüphaneler gereklidir:

```bash
pip install tensorflow numpy Pillow


Kullanım
1-(Varsa) sanal ortamı aktive et:
    conda activate cancer-classification-env
2-Klasöre gir:
    cd Leukemia
3-Tahmin script'ini çalıştır:
    python predict.py

Tahmin edilecek görsel yolunu predict.py içinden değiştirebilirsin (IMAGE_PATH satırı).

Fonksiyon Açıklamaları (utils.py)
load_saved_model()
Modeli .h5 uzantılı dosyadan yükler.

Sınıf etiketlerini (["Benign", "Early", "Pre", "Pro"]) birlikte döndürür.


prepare_image(image_path, target_size=(224, 224))
Görseli load_img ile yükler

img_to_array ile NumPy array'e çevirir

preprocess_input ile normalize eder (ResNet50 formatına uygun)

Batch boyutu ekler → (1, 224, 224, 3)

Çıktı:
Modelin girişine verilebilecek biçimde görüntü array’i


predict_image(image_array, model, class_names)
Modelle tahmin yapar (model.predict)

En yüksek olasılığı bulur (np.argmax)

İlgili sınıf etiketini class_names listesinden çeker