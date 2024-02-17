import unittest

from png_checker import is_too_wide


class TestPngChecker(unittest.TestCase):
    def test_is_too_widek(self):
        self.assertFalse(is_too_wide("test/data_png/ok.png"))
        self.assertTrue(is_too_wide("test/data_png/ng.png"))
