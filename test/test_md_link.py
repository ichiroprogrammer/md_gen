import unittest

from md_link import get_args, gen_fc
from md_lib.file_container import FileContainer


class TestMdLink(unittest.TestCase):
    def test_args(self):
        act0 = get_args("-o out in --db db.json".split(" "))
        exp0 = {"md": "in", "o": "out", "db": "db.json", "ig": None, "sec_num": False}
        print(act0)
        self.assertEqual(exp0, act0)

    def test_gen_fc(self):
        in_md = "test/data/simple1_anchor.md"
        out_md = "test/resolved/simple1_anchor.md"
        db = "test/data/simple_all_sec.json"

        fc_exp0 = FileContainer(out_md)
        fc_act0 = gen_fc(get_args(f"-o {out_md} {in_md} --db {db}".split(" ")))
        self.assertEqual(fc_exp0, fc_act0)

    def test_gen_fc2(self):
        in_md = "test/data/simple1_anchor_no_sub.md"
        out_md = "test/resolved/simple1_anchor.md"
        db = "test/data/simple_all_sec.json"

        fc_exp0 = FileContainer(out_md)
        fc_act0 = gen_fc(get_args(f"-o {out_md} {in_md} --db {db}".split(" ")))
        self.assertEqual(fc_exp0, fc_act0)
