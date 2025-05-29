import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""
        title = extract_title(md)
        self.assertEqual(title, "this is an h1")







if __name__ == "__main__":
    unittest.main()