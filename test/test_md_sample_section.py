import unittest

from md_sample_section import get_args, gen_fc
from md_lib.file_container import FileContainer


class TestMdMakeSampleSection(unittest.TestCase):
    def test_args(self):
        act0 = get_args("-o sample.md --python p m1 m2 m3".split(" "))
        exp0 = {
            "mds": ["m1", "m2", "m3"],
            "python": "p",
            "o": "sample.md",
        }
        self.assertEqual(exp0, act0)

    def test_gen_fc(self):
        out = "test/data/sample_sec_2.md"
        args = get_args(
            f"-o {out} "
            "--python test/ "
            "test/resolved/simple1_anchor.md "
            "test/resolved/simple2_anchor.md "
            "test/data/code_ref_no_code.md".split(" ")
        )

        fc_act = gen_fc(args)
        fc_exp = FileContainer(out)
        self.assertEqual(fc_exp, fc_act)

        out = "test/data/sample_sec_3.md"
        args = get_args(
            f"-o {out} "
            "--python test/ "
            "test/resolved/simple1_anchor.md "
            "test/resolved/simple2_anchor.md "
            "test/data/code_ref_no_code.md".split(" ")
        )

        fc_act = gen_fc(args)
        fc_exp = FileContainer(out)
        self.assertEqual(fc_exp, fc_act)
