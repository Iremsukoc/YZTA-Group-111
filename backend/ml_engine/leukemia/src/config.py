import os

# Proje kök dizini
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Veri klasörü (senin 'Original' veri setin burada olacak)
DATA_DIR = os.path.join(BASE_DIR, 'data', 'Original')

# Model ve etiket dosyalarının kaydedileceği yollar
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'resnet50.h5')
LABEL_ENCODER_PATH = os.path.join(BASE_DIR, 'models', 'label_classes.npy')

# Çıktı görsellerinin kaydedileceği klasör
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')

# Sınıf isimleri (veri klasöründeki alt klasör adlarıyla birebir aynı olmalı)
CLASS_NAMES = ['Benign', 'Pre', 'Pro', 'Early']
