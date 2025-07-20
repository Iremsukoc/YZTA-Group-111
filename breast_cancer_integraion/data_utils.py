from torchvision import datasets, transforms
from torch.utils.data import DataLoader
from config import *
from PIL import Image  # This is very important

def get_dataloaders():
    data_transforms = transforms.Compose([
    transforms.Resize((IMG_SIZE, IMG_SIZE)),
    transforms.Lambda(lambda img: img.convert("RGB")), #Converts from Grayscale to RGB.
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5],
                         [0.5, 0.5, 0.5])
])


    ...

    data_dir = "data/breast_cancer_dataset_split"

    train_dataset = datasets.ImageFolder(root=f"{data_dir}/train", transform=data_transforms)
    val_dataset   = datasets.ImageFolder(root=f"{data_dir}/val",   transform=data_transforms)
    test_dataset  = datasets.ImageFolder(root=f"{data_dir}/test",  transform=data_transforms)

    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader   = DataLoader(val_dataset,   batch_size=BATCH_SIZE, shuffle=False)
    test_loader  = DataLoader(test_dataset,  batch_size=BATCH_SIZE, shuffle=False)

    return train_loader, val_loader, test_loader
