import unittest

from md_to_html import get_args, gen_fc
from md_lib.file_container import FileContainer


class TestMdMakeSampleSection(unittest.TestCase):
    def test_args(self):
        act0 = get_args("-o o.md in.md --title T00 --author xxx".split(" "))
        exp0 = {
            "author": "xxx",
            "md": "in.md",
            "title": "T00",
            "o": "o.md",
        }
        self.assertEqual(exp0, act0)

    def test_gen_fc(self):
        html = "test/data/simple123_join.html"
        md = "test/data/simple123_join.md"

        args = get_args(f"-o {html} {md} --title T00 --author xxx".split(" "))

        fc_act = gen_fc(args)
        fc_exp = FileContainer(html)
        self.assertEqual(fc_exp, fc_act)

        ###

        index_md = "test/data/simple_all_add_sc_index.md"
        index_html = "test/data/simple_all_add_sc_index.html"

        args = get_args(
            f"-o {index_html} {index_md} --title T00 --author xxx".split(" ")
        )
        fc_act = gen_fc(args)

        fc_act = gen_fc(args)
        fc_exp = FileContainer(index_html)
        self.assertEqual(fc_exp, fc_act)
