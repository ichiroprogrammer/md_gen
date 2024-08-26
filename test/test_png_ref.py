import unittest
from pprint import pprint

from md_lib.file_container import FileContainer
from md_lib.png_ref import get_png_in_link, change_png_link_to_base64


class TestPngLink(unittest.TestCase):
    def test_get_png_in_link(self):
        test_data = [
            (
                "![hehe](data_pu/rectangle_square.png)\n",
                "data_pu/rectangle_square.png",
            ),
            ("![hehe](data_pu/rectangle_square.png)", None),
            ("[hehe](data_pu/rectangle_square.png)", None),
        ]

        for org, exp in test_data:
            act = get_png_in_link("./some_md_file.md", org)
            self.assertEqual(exp, act)

    def test_change_png_link_to_base64(self):
        fc_org = FileContainer("test/data/include_test.md")

        fc_act = change_png_link_to_base64(fc_org)
        fc_exp = FileContainer("test/data/include_test_base64.md")

        self.assertEqual(fc_exp.content, fc_act.content)
