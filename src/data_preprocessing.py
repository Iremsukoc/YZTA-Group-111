import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import warnings
warnings.filterwarnings("ignore")

def train_df(tr_path):
    classes, class_paths = zip(*[(label, os.path.join(tr_path, label, image))
                                 for label in os.listdir(tr_path) if os.path.isdir(os.path.join(tr_path, label))
                                 for image in os.listdir(os.path.join(tr_path, label))])
    return pd.DataFrame({'Class Path': class_paths, 'Class': classes})

def plot_class_distribution(train_dir):
    tr_df = train_df(train_dir)
    plt.figure(figsize=(15, 7))
    ax = sns.countplot(data=tr_df, y=tr_df['Class'])
    plt.xlabel('')
    plt.ylabel('')
    plt.title('Count of images in each class', fontsize=20)
    ax.bar_label(ax.containers[0])
    plt.show()

def create_data_loaders(data_dir, img_size, batch_size):
    
    # Data augmentation and normalization
    train_transforms = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.RandomRotation(20),
        transforms.RandomHorizontalFlip(),
        transforms.RandomAffine(degrees=0, translate=(0.1, 0.1), scale=(0.9, 1.1)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    test_transforms = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    train_dataset = datasets.ImageFolder(os.path.join(data_dir, 'Training'), transform=train_transforms)
    test_dataset = datasets.ImageFolder(os.path.join(data_dir, 'Testing'), transform=test_transforms)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=4)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, num_workers=4)

    return train_loader, test_loader
