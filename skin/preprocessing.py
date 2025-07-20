from torchvision import transforms

def get_train_transform(img_size=112):
    """
    Returns torchvision transforms for training data augmentation.
    """
    return transforms.Compose([
        transforms.RandomRotation(degrees=20),
        transforms.RandomHorizontalFlip(p=0.3),
        transforms.RandomVerticalFlip(p=0.3),
        transforms.Resize(size=(img_size, img_size), antialias=True),
        transforms.CenterCrop(size=(img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

def get_val_transform(img_size=112):
    """
    Returns torchvision transforms for validation/testing.
    """
    return transforms.Compose([
        transforms.Resize(size=(img_size, img_size), antialias=True),
        transforms.CenterCrop(size=(img_size, img_size)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
