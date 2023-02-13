from pathlib import Path
import os

def get_dataset(base_path: str = 'output_split'):
    """
    Get Dataset for training
    """
    base_path = Path(base_path)
    dataset = []

    for file in os.listdir(base_path):
        if '_mask' in file:
            base_file = file.replace('_mask', '')
            if os.path.exists(base_path / base_file):
                dataset.append((base_path / base_file, base_path / file))
            else:
                print(f'Warning, found mask but no base file for {file}.')
    return dataset