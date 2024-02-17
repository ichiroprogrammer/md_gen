import unittest

from md_join import get_args, gen_fc
from md_lib.file_container import FileContainer


class TestMdJoin(unittest.TestCase):
    def test_args(self):
        act0 = get_args("-o out other0 other1 other2".split(" "))
        exp0 = {"mds": ["other0", "other1", "other2"], "o": "out"}
        self.assertEqual(exp0, act0)

    def test_gen_fc(self):
        out = "test/data/simple123_join.md"

        args0 = get_args(
            f"-o {out} test/data/simple1_anchor.md test/data/simple2_anchor.md test/data/simple3_anchor.md".split(
                " "
            )
        )
        fc_act0 = gen_fc(args0)
        fc_exp0 = FileContainer(out)

        self.assertEqual(fc_exp0, fc_act0)
