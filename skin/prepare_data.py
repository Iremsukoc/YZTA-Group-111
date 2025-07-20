"""
Script for preparing and organizing raw data for skin cancer classification.
"""
import argparse
import yaml
import os
import random
import shutil
# import os, shutil, etc. as needed

def split_train_val(train_dir, val_dir, val_ratio=0.15, seed=42):
    random.seed(seed)
    classes = [d for d in os.listdir(train_dir) if os.path.isdir(os.path.join(train_dir, d))]
    for cls in classes:
        src = os.path.join(train_dir, cls)
        dst = os.path.join(val_dir, cls)
        os.makedirs(dst, exist_ok=True)
        files = [f for f in os.listdir(src) if f.endswith('.jpg')]
        random.shuffle(files)
        n_val = int(len(files) * val_ratio)
        val_files = files[:n_val]
        for f in val_files:
            shutil.move(os.path.join(src, f), os.path.join(dst, f))
        print(f"Moved {n_val} images from {src} to {dst}")

def prepare_data(config):
    """
    Prepares data for training (e.g., splitting, organizing folders).
    Args:
        config (dict): Configuration dictionary.
    """
    # Split train into train/val
    split_train_val(config['data']['train_dir'], config['data']['val_dir'], val_ratio=0.15, seed=config['train'].get('seed', 42))
    print("Validation split completed.")
    # TODO: Implement other data preparation logic if needed
    pass

def parse_args():
    parser = argparse.ArgumentParser(description='Prepare data for skin cancer classification')
    parser.add_argument('--config', type=str, default='configs/config.yaml', help='Path to config file')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    with open(args.config, 'r') as f:
        config = yaml.safe_load(f)
    prepare_data(config)
