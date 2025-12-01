import dataset
from seed_dataset import data_subset
import torch


def ann_test1(dataset_path: str, training_steps: int):
    data = data_subset(dataset_path, -1) # Get all data


if __name__ == "__main__":
    step_count = 16
    ann_test1("datasets/jane-eyre", step_count)
