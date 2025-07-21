from src.data.data_loader import load_data_from_directory
from src.preprocessing.image_generators import create_generators
from src.model.train import train_model
from src.evaluation.visuals import plot_history
from src.evaluation.metrics import evaluate_model  # <-- metrikler için eklendi

# Parametreler
IMG_SIZE = (128, 128)
COLOR_MODE = "grayscale"
BATCH_SIZE = 16
EPOCHS = 50
NUM_CLASSES = 3

# Etiket isimleri
label_map = {0: 'Benign cases', 1: 'Malignant cases', 2: 'Normal cases'}

# Veriyi yükle
df = load_data_from_directory("data")

# Veriyi generatörlere ayır
train_gen, val_gen, test_gen = create_generators(
    df,
    img_height=IMG_SIZE[0],
    img_width=IMG_SIZE[1],
    batch_size=BATCH_SIZE,
    color_mode=COLOR_MODE
)

# Modeli eğit
input_shape = (IMG_SIZE[0], IMG_SIZE[1], 1 if COLOR_MODE == "grayscale" else 3)
model, history = train_model(train_gen, val_gen, input_shape, NUM_CLASSES, EPOCHS)

# Eğitim geçmişini çiz
plot_history(history)

# Modeli kaydet
model.save("lung_cancer_cnn.keras")
model.save("lung_cancer_cnn.h5")

# Test seti üzerinde modeli değerlendir
evaluate_model(model, test_gen, label_map)
