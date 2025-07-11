# Brain Tumor Classification

This project implements a deep learning model to classify brain tumors into four categories (`glioma`, `meningioma`, `notumor`, `pituitary`) using the Kaggle "Brain Tumor MRI Dataset" with PyTorch. The model is a custom CNN designed for high accuracy on MRI images, leveraging GPU acceleration (e.g., NVIDIA RTX 4060).

## Project Overview
- **Dataset**: [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset)
- **Model**: Custom Convolutional Neural Network (CNN) with Conv2d, MaxPool2d, Linear, and Dropout layers.
- **Optimizer**: Adamax
- **Loss**: CrossEntropyLoss
- **Metrics**: Accuracy, Precision, Recall, and optional F1 Score (micro/macro).
- **Hardware**: Optimized for GPU usage (CUDA support).

## Directory Structure
```
brain_tumor_classification/
├── data/
│   ├── Training/
│   │   ├── glioma/
│   │   ├── meningioma/
│   │   ├── notumor/
│   │   └── pituitary/
│   ├── Testing/
│   │   ├── glioma/
│   │   ├── meningioma/
│   │   ├── notumor/
│   │   └── pituitary/
├── models/              # Saved model weights (e.g., saved_model.pth, saved_model_final.pth)
├── results/             # Training plots (training_plot.png) and confusion matrix (confusion_matrix.png)
├── src/
│   ├── __init__.py      # Module initialization
│   ├── data_preprocessing.py  # Data loading and augmentation
│   ├── model_training.py      # Model definition and training
│   ├── evaluation.py          # Model evaluation and visualization
│   ├── main.py               # Main execution script
└── visualize_predictions.py # Predict images
├── test_best_model.py    # Test the best saved model
├── config.yaml           # Configuration parameters
├── requirements.txt      # Project dependencies
└── README.md             # Project documentation
```

## Setup
### Prerequisites
- Python 3.10

### Installation
1. Clone the repository or set up the project directory:
   ```bash
   git clone <repository-url> 
   cd brain_tumor_classification
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Dataset
- Download the [Brain Tumor MRI Dataset](https://www.kaggle.com/datasets/masoudnickparvar/brain-tumor-mri-dataset) from Kaggle.
- Extract and place the data in the `data/` directory with the structure shown above.

## Usage
### Train the Model
Run the main script to train the model:
```bash
python src/main.py
```
- This will train the model for the number of epochs specified in `config.yaml`, save the best model to `models/saved_model.pth`, and generate plots in `results/`.

### Evaluate the Best Model
Test the saved best model:
```bash
python src/test_best_model.py
```
*   This script loads `models/saved_model.pth` and evaluates it on the test set.
  
*   Evaluation results include accuracy, precision, recall, and confusion matrix.

- You can download the best-performing model from the link below and place it under the models/ directory:

 - [Download saved_model.pth](https://drive.google.com/file/d/13hQEPX7O3azxYCN58cjzwe4iwGbJaaT6/view?usp=drive_link)

### Visualize Predictions
Visualize random predictions from the test set:
```bash
python src/visualize_predictions.py
```
- This displays 5 random images with their true and predicted labels.

## Configuration
Edit `config.yaml` to adjust parameters:
```yaml
data_dir: ./data
img_size: 224
batch_size: 32
epochs: 30
model_path: ./models/saved_model.pth
```

## Results
- **Training Plots**: Saved as `results/training_plot.png` (accuracy, loss, precision, recall over epochs).
- **Confusion Matrix**: Saved as `results/confusion_matrix.png` after evaluation.
- **Model Performance**: Metrics (accuracy, precision, recall) are printed to the console.

## Notes
- The model uses GPU acceleration if available (`cuda`). Check with `python -c "import torch; print(torch.cuda.is_available())"`.
*  For progress bars during training, the code supports tqdm (install via requirements.txt).

*  AUC (ROC-AUC) is optional for multiclass classification; F1 Score (micro) is recommended for imbalanced datasets.
  
