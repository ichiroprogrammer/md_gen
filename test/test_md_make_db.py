import unittest

from md_make_db import get_args, gen_db
from md_lib.link_ref import load_db
from md_lib.file_container import FileContainer


class TestMdMakeDb(unittest.TestCase):
    def test_args(self):
        act0 = get_args("db.json --mds a1 a2 a3".split(" "))
        exp0 = {"db": "db.json", "mds": ["a1", "a2", "a3"]}
        self.assertEqual(exp0, act0)

    def test_gen_fc(self):
        md1 = "test/data/simple1_anchor.md"
        md2 = "test/data/simple2_anchor.md"
        md3 = "test/data/simple3_anchor.md"

        db = "test/data/simple_all_sec.json"

        content_act = gen_db(get_args(f"{db} --mds {md1} {md2} {md3}".split(" ")))
        content_exp = load_db(db)

        self.assertEqual(content_exp, content_act)
