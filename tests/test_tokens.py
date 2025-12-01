import unittest


class Tokens(unittest.TestCase):
    def token_set(self):
        """Test src/utils/token_set.py."""
        from src.utils.token_set import seed_tokens
        from src.utils.token_set import seed_tokens_to_file
        from src.utils.token_set import get_tokens_from_file

        # Get sample data.
        with open("../datasets/test/bean.txt", "r") as test_sample_text_file:
            test_sample_text = test_sample_text_file.read()

        tokens_file_path = "test_files/test_tokens.txt"

        # Slow (not fast)
        tokens = seed_tokens(test_sample_text, silent=True)
        seed_tokens_to_file(tokens_file_path, tokens=tokens, silent=True)
        self.assertListEqual(get_tokens_from_file(tokens_file_path), tokens)
        seed_tokens_to_file(tokens_file_path, text=test_sample_text, silent=True)
        self.assertListEqual(get_tokens_from_file(tokens_file_path), tokens)

        # Fast
        tokens = seed_tokens(test_sample_text, fast=True, silent=True)
        seed_tokens_to_file(tokens_file_path, tokens=tokens, silent=True)
        self.assertListEqual(get_tokens_from_file(tokens_file_path), tokens)
        seed_tokens_to_file(tokens_file_path, text=test_sample_text, fast=True, silent=True)
        self.assertListEqual(get_tokens_from_file(tokens_file_path), tokens)

    def tokenise(self):
        """Test src/utils/tokenise.py."""
        from src.utils.tokenise import tokenise
        from src.utils.tokenise import detokenise

        # Get sample data.
        with open("../datasets/test/bean.txt", "r") as test_sample_text_file:
            test_sample_text = test_sample_text_file.read()

        tokens_file_path = "test_files/test_tokens.txt"

        # Test with test_tokens.txt
        tokens = tokenise(test_sample_text, tokens_path=tokens_file_path)
        text = detokenise(tokens, tokens_path=tokens_file_path)
        self.assertEqual(test_sample_text.lower().replace('\n', ' '), text.lower())

        # Test with default tokens file
        tokens = tokenise(test_sample_text)
        text = detokenise(tokens)
        self.assertEqual(test_sample_text.lower().replace('\n', ' '), text.lower())


if __name__ == '__main__':
    unittest.main()
