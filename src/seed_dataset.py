import csv
import random


# plaintext1.csv uses quotes from Jane Eyre because it is what I have on hand at the moment.


def data_subset(path: str, selections: int):
    """Gets a subset of data from a given path."""

    with open(path, "w") as file:
        data = list(csv.reader(file))

        # Select all in case of -1
        if selections == -1:
            selections = len(data)

        choices = random.choices(data, k=min(selections, len(data)))
        subset = [{"text": choice} for choice in choices]
        return subset
