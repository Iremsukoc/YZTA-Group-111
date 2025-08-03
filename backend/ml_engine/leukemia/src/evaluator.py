import numpy as np
from sklearn.metrics import (
    f1_score, precision_score, recall_score, cohen_kappa_score,
    classification_report, confusion_matrix, roc_curve, auc
)
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
import seaborn as sns

from config import CLASS_NAMES, OUTPUT_DIR

def evaluate_model(model, X_test, y_test, label_encoder):
    y_pred_probs = model.predict(X_test)
    y_pred_classes = np.argmax(y_pred_probs, axis=1)

    f1 = f1_score(y_test, y_pred_classes, average='weighted')
    precision = precision_score(y_test, y_pred_classes, average='weighted')
    recall = recall_score(y_test, y_pred_classes, average='weighted')
    kappa = cohen_kappa_score(y_test, y_pred_classes)

    print(f"F1 Score: {f1:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"Cohen's Kappa: {kappa:.4f}")
    print(classification_report(y_test, y_pred_classes, target_names=CLASS_NAMES))

    # Confusion Matrix
    cm = confusion_matrix(y_test, y_pred_classes)
    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=CLASS_NAMES, yticklabels=CLASS_NAMES)
    plt.title("Confusion Matrix")
    plt.xlabel("Predicted")
    plt.ylabel("True")
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/confusion_matrix.png")
    plt.close()

    # ROC Curve
    y_test_bin = label_binarize(y_test, classes=range(len(CLASS_NAMES)))

    fpr = dict()
    tpr = dict()
    roc_auc = dict()

    for i in range(len(CLASS_NAMES)):
        fpr[i], tpr[i], _ = roc_curve(y_test_bin[:, i], y_pred_probs[:, i])
        roc_auc[i] = auc(fpr[i], tpr[i])

    plt.figure()
    for i in range(len(CLASS_NAMES)):
        plt.plot(fpr[i], tpr[i], lw=2, label=f'{CLASS_NAMES[i]} (AUC = {roc_auc[i]:.2f})')

    plt.plot([0, 1], [0, 1], 'k--')
    plt.title('ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.legend(loc='lower right')
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/roc_curve.png")
    plt.close()
