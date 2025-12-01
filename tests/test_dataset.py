import unittest


class Dataset(unittest.TestCase):
    def seed_dataset(self):
        """Test src/seed_dataset.py."""
        from src.dataset import TextDataset
        from src.seed_dataset import text_dataset, text_dataset_subset

        # Create dataset.
        with text_dataset("datasets/test") as dataset:
            self.assertIsInstance(dataset, TextDataset)

            # Take subsets
            subset = text_dataset_subset(dataset, 0)
            self.assertIsInstance(subset, list)
            self.assertEqual(len(subset), 0)

            subset = text_dataset_subset(dataset, 1)
            self.assertEqual(len(subset), 1)

            subset = text_dataset_subset(dataset, 2)
            self.assertIsInstance(subset, list[tuple])
            self.assertIsInstance(subset[0][0], str)
            self.assertEqual(len(subset), 2)

            subset = text_dataset_subset(dataset, 4)
            self.assertEqual(len(subset), 4)
            subset = text_dataset_subset(dataset, -1)
            self.assertIsInstance(subset, list[tuple])
            self.assertIsInstance(subset[0][0], str)
            self.assertEqual(len(subset), 5)

            # Test len function
            self.assertEqual(len(dataset), 5)


if __name__ == '__main__':
    unittest.main()
