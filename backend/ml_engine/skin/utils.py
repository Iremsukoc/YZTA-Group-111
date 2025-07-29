"""
Utility functions for skin cancer classification project.
"""

def binary_accuracy(outputs, targets):
    """
    Computes the accuracy for binary classification with logits.
    Args:
        outputs: Model outputs (logits), shape (N, 1)
        targets: Ground truth labels, shape (N, 1)
    Returns:
        Accuracy (float)
    """
    preds = (outputs.sigmoid() > 0.5).float()
    correct = (preds == targets).float().sum()
    return correct / targets.numel()

# TODO: Add helper functions for metrics, logging, visualization, etc.
