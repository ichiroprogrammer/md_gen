import unittest

from md_make_index import get_args, gen_fc
from md_lib.file_container import FileContainer


class TestMdMakeDb(unittest.TestCase):
    def test_args(self):
        act0 = get_args("db.json -o a1.index".split(" "))
        exp0 = {
            "db": "db.json",
            "o": "a1.index",
            "sec_num": False,
            "excerpt": None,
            "exclude": None,
        }
        self.assertEqual(exp0, act0)

    def test_gen_fc(self):
        # test/data/simple_all_add_sc.jsonの作り方
        # cd test/data
        # ../../export/py/md_make_db.py simple_all_add_sc.json --mds simple1_anchor.md
        #        simple2_anchor.md sample_code.md

        db = "test/data/simple_all_add_sc.json"
        md_index = "test/data/simple_all_add_sc_index.md"

        fc_act = gen_fc(
            get_args(
                f"{db} -o {md_index} --exclude sample_code.md:2 "
                "--excerpt simple2_anchor.md:2".split(" ")
            )
        )

        fc_exp = FileContainer(md_index)

        self.assertEqual(fc_exp.filename, fc_act.filename)
        self.assertEqual(fc_exp.content, fc_act.content)

        md_index = "test/data/simple_all_add_sc_index_sec_num.md"

        fc_act = gen_fc(
            get_args(
                f"{db} --sec_num -o {md_index} --exclude sample_code.md:2".split(" ")
            )
        )
        fc_exp = FileContainer(md_index)

        self.assertEqual(fc_exp, fc_act)
