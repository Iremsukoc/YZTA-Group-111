import os
import pandas as pd

def load_data_from_directory(base_dir):
    """
    Klasör yapısındaki tüm görselleri ve etiketlerini okur.
    
    Args:
        base_dir (str): Ana klasör (örnek: 'data')
        
    Returns:
        pd.DataFrame: filename ve label sütunlarına sahip tablo
    """
    filepaths = []
    labels = []

    for label in os.listdir(base_dir):
        class_dir = os.path.join(base_dir, label)
        if os.path.isdir(class_dir):
            for file in os.listdir(class_dir):
                filepaths.append(os.path.join(class_dir, file))
                labels.append(label)

    df = pd.DataFrame({'filename': filepaths, 'label': labels})
    return df
