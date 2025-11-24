import unittest
from src.seed_dataset import data_subset


class Dataset(unittest.TestCase):
    def seed_dataset(self):
        subset = data_subset("datasets.plaintext1.csv", -1)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
