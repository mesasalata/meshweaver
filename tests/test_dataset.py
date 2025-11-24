import unittest
from src.seed_dataset import data_subset


class Dataset(unittest.TestCase):
    def seed_dataset(self):
        subset = data_subset("datasets.plaintext1.csv", -1)
        self.assertIsInstance(subset, list)
        self.assertIsInstance(subset[0], tuple)
        self.assertIsInstance(subset[0][0], str)


if __name__ == '__main__':
    unittest.main()
