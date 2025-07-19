import os
import shutil
import random

# Input and output directories
SOURCE_DIR = r"C:\Users\muham\Downloads\breast_cancer_project_pytorch\breast_cancer_dataset\breast_cancer_project_ds\Dataset_BUSI_with_GT"
TARGET_DIR = r"C:\Users\muham\Downloads\breast_cancer_project_pytorch\breast_cancer_dataset_split"
CLASSES = ["benign", "malignant", "normal"]

SPLIT_RATIOS = {
    "train": 0.7,
    "val": 0.15,
    "test": 0.15
}

def create_dirs():
    for split in SPLIT_RATIOS:
        for cls in CLASSES:
            os.makedirs(os.path.join(TARGET_DIR, split, cls), exist_ok=True)

def split_and_copy():
    random.seed(42)
    create_dirs()

    for cls in CLASSES:
        src_path = os.path.join(SOURCE_DIR, cls)
        images = [f for f in os.listdir(src_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
        total = len(images)
        if total == 0:
            print(f"Warning: {cls} folder is empty!")
            continue

        random.shuffle(images)
        train_end = int(total * SPLIT_RATIOS["train"])
        val_end = train_end + int(total * SPLIT_RATIOS["val"])

        splits = {
            "train": images[:train_end],
            "val": images[train_end:val_end],
            "test": images[val_end:]
        }

        for split_name, split_files in splits.items():
            for fname in split_files:
                src_file = os.path.join(src_path, fname)
                dst_file = os.path.join(TARGET_DIR, split_name, cls, fname)
                shutil.copy2(src_file, dst_file)

        print(f"{cls}: Total {total} → train {len(splits['train'])}, val {len(splits['val'])}, test {len(splits['test'])}")

    print(" Split operation completed.")

if __name__ == "__main__":
    split_and_copy()
