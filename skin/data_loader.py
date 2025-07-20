"""
Handles loading datasets for training and validation using torchvision.datasets.ImageFolder.
"""

from torchvision import datasets
from torch.utils.data import DataLoader

def get_dataloaders(train_dir, val_dir, train_transform, val_transform, batch_size=32, num_workers=4):
    """
    Returns PyTorch DataLoader objects for train and validation splits.
    Args:
        train_dir (str): Path to training data directory.
        val_dir (str): Path to validation data directory.
        train_transform: torchvision transforms for training.
        val_transform: torchvision transforms for validation.
        batch_size (int): Batch size for DataLoader.
        num_workers (int): Number of worker processes.
    Returns:
        train_loader, val_loader
    """
    # Load datasets using ImageFolder
    train_dataset = datasets.ImageFolder(root=train_dir, transform=train_transform)
    val_dataset = datasets.ImageFolder(root=val_dir, transform=val_transform)

    # Create DataLoaders
    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=num_workers)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)

    return train_loader, val_loader

def get_test_loader(test_dir, test_transform, batch_size=32, num_workers=4):
    """
    Returns PyTorch DataLoader object for test split.
    Args:
        test_dir (str): Path to test data directory.
        test_transform: torchvision transforms for test data.
        batch_size (int): Batch size for DataLoader.
        num_workers (int): Number of worker processes.
    Returns:
        test_loader
    """
    test_dataset = datasets.ImageFolder(root=test_dir, transform=test_transform)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=num_workers)
    return test_loader
