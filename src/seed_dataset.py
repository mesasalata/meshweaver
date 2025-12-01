import csv
import random
from dataset import TextDataset


# Dataset uses quotes from Jane Eyre because it is what I have on hand at the moment.


def data_subset_csv(path: str, selections: int) -> list:
    """Gets a subset of data from a given path. Depreciated."""

    with open(path, "r") as file:
        data = list(csv.reader(file))[1:]

        # Select all in case of -1
        if selections == -1:
            selections = len(data)

        choices = random.choices(data, k=min(selections, len(data)))
        subset = [{"text": choice} for choice in choices]
        return subset


def read(path: str):
    with open(path, "r") as file:
        return file.read()


def text_dataset(path) -> TextDataset:
    """Utility function for generating a dataset."""

    return TextDataset(path + "/index.csv", path, read)


def text_dataset_subset(dataset: TextDataset, selections: int) -> list[tuple]:
    """Gets a subset of data from a given text dataset."""

    data_count = len(dataset)

    # Select all in case of -1
    if selections == -1:
        selections = data_count

    # Choose indices
    choices = random.choices(range(data_count), k=min(selections, data_count))
    subset = [dataset[choice] for choice in choices]

    return subset
