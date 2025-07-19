# Breast Cancer Classification with ResNet101

This repository provides a deep learning pipeline for classifying breast cancer using the BUSI with GT ultrasound image dataset. The model is based on the ResNet101 architecture, and its performance is evaluated using accuracy and F1-score metrics.

---

## Project Structure

```
breast_cancer_project_pytorch/
├── data/
│   ├── breast_cancer_dataset/              # Original BUSI dataset
│   └── breast_cancer_dataset_split/        # Train/Validation/Test split
├── saved_model/
│   └── best_model.pth                      # Best model checkpoint
├── src/
│   ├── config.py                           # Hyperparameters and settings
│   ├── data_utils.py                       # Dataloader utilities
│   ├── model.py                            # Model definition (ResNet101)
│   ├── train.py                            # Training script
│   ├── predict_single_image.py             # Single image inference
│   └── llm_inference.py                    # (Optional) LLM-based result interpretation
├── .env                                    # Environment variables (not tracked by Git)
├── .gitignore                              # Files and folders to ignore
└── requirements.txt                        # Python dependencies
```

---

## Download Pretrained Model

You can download the latest trained model checkpoint from the following link:

[Download best_model.pth](https://your-download-link.com/best_model.pth)

Place the downloaded file in the `saved_model/` directory.

---

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Iremsukoc/YZTA-Bootcamp.git
cd YZTA-Bootcamp
git checkout -b ml-1.0.2/image-classification-core
cd breast_cancer_project_pytorch
```

### 2. Create a Virtual Environment and Install Dependencies

```bash
conda create -n breast_cancer python=3.10 -y
conda activate breast_cancer
pip install -r requirements.txt
```

Note: [MLflow](https://mlflow.org/) is integrated for experiment tracking. During training, metrics, parameters, and model checkpoints are automatically logged. To launch the MLflow UI, run:

```bash
mlflow ui
```

Then, visit [http://localhost:5000](http://localhost:5000) in your browser to visualize your experiments.

---

## Model Details

- Model: ResNet101
- Loss Function: CrossEntropyLoss
- Optimizer: Adam
- Epochs: 50 (configurable)
- The best model is saved as `.pth` under `saved_model/best_model.pth`.

---

## Training the Model

```bash
cd src
python train.py
```

The `train.py` script trains the model using the settings in `config.py`. All metrics, parameters, and the best model are automatically logged with MLflow during training.

---

## Single Image Prediction

To make a prediction on a random test image, run:

```bash
cd src
python predict_single_image.py
```

The script selects a random image from the test set and predicts its class using the best model checkpoint.

---

## Results

### Training Results

* Train Accuracy: 92.37%
* Validation Accuracy: 89.17%

### Classification Report

| Class        | Precision | Recall | F1-Score | Support |
| ------------ | --------- | ------ | -------- | ------- |
| benign       | 0.91      | 0.87   | 0.89     | 135     |
| malignant    | 0.86      | 0.78   | 0.82     | 64      |
| normal       | 0.75      | 0.95   | 0.84     | 41      |
| Accuracy     |           |        | 0.86     | 240     |

### Confusion Matrix

```
[[122   9    4]
 [ 9    51   4]
 [ 0    2   39]]
```

---

## Technologies Used

* Python 3.10+
* PyTorch
* torchvision
* scikit-learn
* NumPy, Matplotlib
* MLflow

---

## Notes

* The best model is saved under `saved_model/` after each training session.
* You can customize training parameters in `config.py`.
* If CUDA is available, GPU will be used automatically.

