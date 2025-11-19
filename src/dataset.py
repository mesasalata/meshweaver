import os
import pandas as pd
from torch.utils.data import Dataset


class TextDataset(Dataset):
    def __init__(self, annotations_file, text_dir, transform=None, target_transform=None):
        self.text_labels = pd.read_csv(annotations_file)
        self.text_dir = text_dir
        self.transform = transform
        self.target_transform = target_transform

    def __len__(self):
        return len(self.text_labels)

    def __getitem__(self, idx):
        text_path = os.path.join(self.text_dir, self.text_labels.iloc[idx, 0])
        text = text_path
        label = self.text_labels.iloc[idx, 1]
        if self.transform:
            text = self.transform(text)
        if self.target_transform:
            label = self.target_transform(label)
        return text, label
