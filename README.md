Bu proje içerisinde Kolon Kanseri, Akciğer Kanseri ve Lösemi (Kan Kanseri) için geliştirilmiş 3 adet görüntü işleme modeli bulunmaktadır.

```text
Colon/
├── Colon
├── Leukemia
├── Lung
├── requirements.txt
└── README.MD
```

---

# Colon Kanseri Sınıflandırma Modeli

Bu klasör, kolon kanseri görüntülerini sınıflandırmak için eğitilmiş bir derin öğrenme modelini ve tahmin scriptlerini içerir. Model, iki sınıf arasında ayrım yapar:

- `Colon_adenocarcinoma`
- `Colon_benign_tissue`

## Dosya Yapısı
```text
Colon/
├── model_cnn.h5 # Eğitilmiş Keras modeli
├── test_split_colon/ # Test görsellerinin bulunduğu klasör
│ ├── Colon_adenocarcinoma/
│ └── Colon_benign_tissue/
├── utils.py # Görüntü işleme ve tahmin fonksiyonları
├── predict.py # Modeli kullanarak görsel sınıflandırma yapan script
```

## Gerekli Kütüphaneler

- TensorFlow
- Pillow (görsel işleme)
- NumPy

Sanal ortam (Anaconda) kullanılması önerilir.


`conda create --name cancer-ai-env python=3.10`

`conda activate cancer-ai-env`

`pip install tensorflow pillow numpy`


### Kullanım
1-Ortamı aktif hale getir:
    conda activate cancer-ai-env
    
2-Klasöre git:
    cd Colon
    
3-Tahmin yapmak için script'i çalıştır:
    python predict.py


## Script Açıklamaları

### utils.py:

- Görselleri modele uygun hale getirmek (yeniden boyutlandırma, normalize etme vb.) ve tahmin işlemleri için yardımcı fonksiyonları içerir.

## Fonksiyon Açıklamaları (utils.py)

## 1. transform_image(uploaded_image, target_size=(224, 224))

### Amaç:

- Yüklenen bir görseli derin öğrenme modeline uygun hale getirir.

## İşlem adımları:

- Görseli RGB formatına dönüştürür (siyah-beyaz vs. karışmasın diye).
- Belirtilen boyuta (224x224) yeniden boyutlandırır (modelin giriş boyutu).
- Görseli NumPy array’e çevirir.
- Piksel değerlerini 0-1 aralığına normalize eder (/255.0).
- Ekstra bir boyut ekler (batch dimension: [1, 224, 224, 3])

### Kullanıldığı yer:

- predict.py içinde test görseli bu fonksiyonla işlenir.


## 2. predict_image(model, img_array, class_names)

### Amaç:

- İşlenmiş bir görsel üzerinden tahmin yapar.

### İşlem adımları:

model.predict(...) ile sınıf olasılıklarını alır.
- En yüksek olasılığa sahip sınıfın index’ini bulur (np.argmax()).
- Index’e karşılık gelen sınıf adını class_names listesinden çeker.
- O sınıfa ait olasılığı da güven oranı (confidence) olarak verir.


Döndürdüğü:
- Tahmin edilen sınıf etiketi (string)
- Güven oranı (float)


Kullanıldığı yer:
- predict.py içinde model tahmini bu fonksiyonla yapılır.


predict.py:
- Modeli yükler (model_cnn.h5)
- Test görselini işler (test_split_colon/...)
- Tahmin yapar ve sonucu ekrana yazdırır


## Notlar
- Test için örnek görsel yolu predict.py içinde sabit olarak verilmiştir. Farklı bir görsel test etmek istersen image_path satırını değiştirmen yeterlidir.
- Klasör isimleri ve model adı farklıysa predict.py içinde güncelleme yapman gerekir.


---

# Lösemi Hücre Sınıflandırma Modeli

Bu klasör, mikroskop görüntüleri üzerinden lösemi (leukemia) hücrelerini sınıflandırmak için eğitilmiş bir derin öğrenme modelini içerir. Model, ResNet50 tabanlıdır ve 4 farklı hücre evresini tanıyabilir. Modelin boyutu 100mb'dan fazla old
duğu için aşağıda link olarak paylaşılmıştır. Tanıyabildiği kanser türleri:

- `Benign`  → İyi huylu
- `Early`   → Erken evre
- `Pre`     → Ön evre
- `Pro`     → Proliferatif (ileri) evre


## Klasör Yapısı
```text
Leukemia/
├── leukemia_resnet_model.h5 # Eğitilmiş model dosyası     [Model Drive Linki](https://drive.google.com/file/d/12Vjt6pj3pI-jgg8dO1UMNFRE-BR-qTNF/view?usp=sharing)
├── test_split_leukemia/ # Test görselleri
│ ├── Benign/
│ ├── Early/
│ ├── Pre/
│ └── Pro/
├── utils.py # Görsel işleme ve tahmin yardımcıları
├── predict.py # Modeli çalıştırıp tahmin yapan script
```

## Gerekli Kütüphaneler

Bu klasörü çalıştırmak için aşağıdaki kütüphaneler gereklidir:
- pip install tensorflow numpy Pillow


### Kullanım
1-(Varsa) sanal ortamı aktive et:
    conda activate cancer-classification-env
    
2-Klasöre gir:
    cd Leukemia
    
3-Tahmin script'ini çalıştır:
    python predict.py

Tahmin edilecek görsel yolunu predict.py içinden değiştirebilirsin (IMAGE_PATH satırı).

## Fonksiyon Açıklamaları (utils.py)

### load_saved_model()
- Modeli .h5 uzantılı dosyadan yükler.
- Sınıf etiketlerini (["Benign", "Early", "Pre", "Pro"]) birlikte döndürür.
- prepare_image(image_path, target_size=(224, 224))
- Görseli load_img ile yükler
- img_to_array ile NumPy array'e çevirir
- preprocess_input ile normalize eder (ResNet50 formatına uygun)
- Batch boyutu ekler → (1, 224, 224, 3)

### Çıktı:
- Modelin girişine verilebilecek biçimde görüntü array’i


### predict_image(image_array, model, class_names)

- Modelle tahmin yapar (model.predict)
- En yüksek olasılığı bulur (np.argmax)
- İlgili sınıf etiketini class_names listesinden çeker

---

# Lung Kanseri Sınıflandırma Modeli

Bu klasör, akciğer (lung) kanseri teşhisi için geliştirilmiş bir derin öğrenme modelini ve tahmin scriptlerini içerir. Model, X-ray veya benzeri tıbbi görüntüler üzerinden aşağıdaki üç sınıfı ayırt eder:

- `Benign cases` (iyi huylu)
- `Malignant cases` (kötü huylu)
- `Normal cases` (sağlıklı)

---

## Klasör Yapısı
```text
Lung/
├── lung_cancer_cnn.h5 # Eğitilmiş model dosyası
├── test_split_lung/ # Test görselleri
│ ├── Benign cases/
│ ├── Malignant cases/
│ └── Normal cases/
├── utils.py # Görsel işleme ve tahmin yardımcı fonksiyonları
├── predict.py # Modeli yükleyip tahmin yapan script
```

## Gerekli Kütüphaneler

Bu projeyi çalıştırmadan önce aşağıdaki kütüphanelerin kurulu olması gerekir:

- pip install tensorflow pillow opencv-python numpy


## Kullanım
### 1-Ortamı aktive et:
    conda activate cancer-classification-env
    
### 2-Klasöre gir:
    cd Lung
### 3-Tahmin yap:
    python predict.py


## Fonksiyon Açıklamaları (utils.py)
### preprocess_single_image(image_path, target_size=(128, 128), color_mode='grayscale')

### Amaç:

- Modelin beklentisine göre görseli işler (boyutlandırır, normalize eder, kanal ve batch boyutu ekler).


### İşlem adımları:

- Görseli açar (PIL ile).
- grayscale modundaysa gri tonlamaya çevirir.
- Yeniden boyutlandırır (128x128).
- NumPy array'e çevirip float32 tipine getirir.
- 0–1 aralığında normalize eder (/255.0).
- Gerekirse kanal boyutu ([..., 1]) ekler.
- Batch boyutu ([1, ...]) ekler.


Çıktı:

- Modelin tahmin yapabileceği biçimde görsel array’i


### predict_uploaded_image(image_path, model, label_map=None, target_size=(128, 128), color_mode='grayscale')

Amaç:

- Verilen görsel dosyasına model ile tahmin yaptırır.


### İşlem adımları:

- Yukarıdaki preprocess_single_image() fonksiyonu ile işleme yapar.
- model.predict(...) ile sınıf olasılıklarını alır.
- En yüksek olasılığa sahip sınıfı argmax ile bulur.
- label_map verilmişse index yerine etiket ismi döndürür


### Çıktı:

- str: Sınıf etiketi (örneğin: 'Malignant cases')
- veya int: Sınıf index’i (etiket verilmemişse)


### predict.py Açıklaması

Bu dosya şu adımları yapar:

- Model dosyasını (lung_cancer_cnn.h5) yükler
- Test için örnek bir görseli belirler (örneğin: Normal cases/colorjitter (12).jpg)
- utils.py içindeki fonksiyonlarla görüntüyü işler
- Tahmin yapar ve sonucu ekrana yazdırır


## Notlar

- IMAGE_PATH satırında kullanılan örnek görselin gerçekten var olduğuna emin olun.
- Modeliniz farklı boyutlarda eğitildiyse target_size parametresini ona göre değiştirin.
- color_mode yanlış verilirse model giriş boyutuyla uyumsuzluk hatası alırsınız.
