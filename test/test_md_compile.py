import unittest

from md_compile import get_args, gen_fc
from md_lib.file_container import FileContainer


class TestMdCompile(unittest.TestCase):
    def test_args(self):
        act0 = get_args("-o out in --mds other0 other1 other2 -p test/v".split(" "))
        exp0 = {
            "md": "in",
            "mds": ["test/v/other0", "test/v/other1", "test/v/other2"],
            "D": None,
            "o": "out",
        }
        self.assertEqual(exp0, act0)

        act1 = get_args("-o out in -D o/out -p ./vpath".split(" "))
        print(act1)
        exp1 = {"md": "in", "mds": None, "D": "o/out", "o": "out"}
        self.assertEqual(exp1, act1)

    def test_gen_fc(self):
        md = "test/data/code_ref_no_code.md"

        out0 = "test/data/code_ref_comp.md"
        args0 = get_args(f"-o {out0} {md} " f"--mds {md}".split(" "))

        fc_exp0 = FileContainer(out0)
        fc_act0 = gen_fc(args0)
        self.assertEqual(fc_exp0, fc_act0)

        out1 = "test/data/code_ref.d"
        args1 = get_args(f"-o {out1} {md} -D o/{out1}".split(" "))

        fc_exp1 = FileContainer(out1)
        fc_act1 = gen_fc(args1)
        self.assertEqual(fc_exp1, fc_act1)

    def test_gen_fc2(self):
        md = "test/data/code_ref_no_code.md"
        after = "test/data/code_continue.md"

        out0 = "test/data/code_continue_comp.md"
        args0 = get_args(f"-o {out0} {after} " f"--mds {md} {after}".split(" "))

        fc_exp0 = FileContainer(out0)
        fc_act0 = gen_fc(args0)
        self.assertEqual(fc_exp0, fc_act0)
