import unittest


class Misc(unittest.TestCase):
    def logger(self):
        """Test src/utils/logger.py."""
        from src.utils.logger import log

        # Test logger (incomplete)
        log_text = log("Test 0.", "print", silent=True)
        self.assertIsInstance(log_text, str)
        self.assertEqual(log_text[0], "[")
        has = log_text.find("Test 0.")
        self.assertNotEqual(has, -1)

        log_text = log("Test 1.", "info", silent=True)
        self.assertIsInstance(log_text, str)
        self.assertEqual(log_text[0], "[")
        has = log_text.find("Test 1.")
        self.assertNotEqual(has, -1)

        log_text = log("Test 2.", "warn", silent=True)
        self.assertIsInstance(log_text, str)
        self.assertEqual(log_text[0], "[")
        has = log_text.find("Test 2.")
        self.assertNotEqual(has, -1)

        log_text = log("Test 3.", "fail", silent=True)
        self.assertIsInstance(log_text, str)
        self.assertEqual(log_text[0], "[")
        has = log_text.find("Test 3.")
        self.assertNotEqual(has, -1)

        log_text = log("Test 4.", "error", silent=True)
        self.assertIsInstance(log_text, str)
        self.assertEqual(log_text[0], "[")
        has = log_text.find("Test 4.")
        self.assertNotEqual(has, -1)

        log_text = log("Test 5.", "error", custom_color="\033[95m", silent=True)
        self.assertIsInstance(log_text, str)
        self.assertEqual(log_text[0], "[")
        has = log_text.find("Test 5.")
        self.assertNotEqual(has, -1)
        has = log_text.find("\033[95m")
        self.assertNotEqual(has, -1)


if __name__ == '__main__':
    unittest.main()
