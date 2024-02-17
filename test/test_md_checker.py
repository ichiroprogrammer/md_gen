import unittest

from md_lib.file_container import FileContainer
from md_lib.md_checker import MdError, find_error


class TestMdChecker(unittest.TestCase):
    __TEST_MD = "test/data/error.md"

    def test_find_error(self):
        fc = FileContainer(TestMdChecker.__TEST_MD)

        errors = find_error(fc)

        exp = [
            MdError(0, 5, "* error1", "error start"),
            MdError(1, 10, "error3", "* error2.2"),
            MdError(2, 24, "last 2 lines should be space"),
        ]
        self.assertEqual(exp, errors)
