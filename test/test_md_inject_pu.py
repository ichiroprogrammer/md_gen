import unittest

from md_inject_pu import get_args, inject_pu
from md_lib.file_container import FileContainer


class TestInjectPu(unittest.TestCase):
    def test_gen_fc(self):
        in_file = "test/data/include_test_base64.md"
        out_file = "test/data/include_test_base64_pu.md"
        args = get_args(f"{in_file} -o {out_file}".split(" "))
        self.assertEqual(args["md"], in_file)
        self.assertEqual(args["o"], out_file)

        in_md = FileContainer(in_file)
        out_md = inject_pu(args)

        FileContainer(out_file, out_md.content).save()
