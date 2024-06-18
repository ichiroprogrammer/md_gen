from collections import OrderedDict
import unittest
from os import path, remove
import pprint

from md_lib.file_container import FileContainer

from md_lib.link_ref import (
    gen_md_anchor_all,
    gen_md_section_db,
    store_db,
    load_db,
    gen_md_index_md,
    SectionDict,
    change_link_ext,
)


class TestMdLink(unittest.TestCase):
    __ORG_MD1 = "test/data/simple1.md"
    __ANC_MD1 = "test/data/simple1_anchor.md"
    __ANC_MD1_1 = "test/data/simple1_anchor_1.md"
    __RES_MD1 = "test/resolved/simple1_anchor.md"

    __ORG_MD1_ERR1 = "test/data/simple1_err1.md"

    __ORG_MD2 = "test/data/simple2.md"
    __ANC_MD2 = "test/data/simple2_anchor.md"
    __ANC_MD2_SEQ = "test/data/simple2_anchor_seq.md"
    __RES_MD2 = "test/resolved/simple2_anchor.md"

    __ORG_MD3 = "test/data/simple3.md"
    __ANC_MD3 = "test/data/simple3_anchor.md"
    __ANC_MD3_SEQ = "test/data/simple3_anchor_seq.md"
    __RES_MD3 = "test/resolved/simple3_anchor.md"

    __ORG_MD3_CONT = "test/data/simple3_cont.md"
    __ANC_MD3_CONT = "test/data/simple3_cont_anchor.md"

    __EXP_JSON = "test/data/simple_all_sec.json"
    __ACT_JSON = "test/data/simple_all_sec.cp.json"

    __EXP_INDEX_MD = "test/data/simple_index.md"

    def setUp(self):
        if path.exists(TestMdLink.__ACT_JSON):
            remove(TestMdLink.__ACT_JSON)

    def tearDown(self):
        if path.exists(TestMdLink.__ACT_JSON):
            remove(TestMdLink.__ACT_JSON)

    def test_gen_md_anchor(self):
        for org, exp in [
            (TestMdLink.__ORG_MD1, TestMdLink.__ANC_MD1),
            (TestMdLink.__ORG_MD1, TestMdLink.__ANC_MD1_1),
            (TestMdLink.__ORG_MD2, TestMdLink.__ANC_MD2),
            (TestMdLink.__ORG_MD3, TestMdLink.__ANC_MD3),
        ]:
            fc_act = gen_md_anchor_all([FileContainer(org)])
            fc_exp = FileContainer(exp)

            self.assertEqual(fc_exp.content, fc_act[0].content)

    def test_gen_md_anchor2(self):
        mds = [
            FileContainer(TestMdLink.__ORG_MD1),
            FileContainer(TestMdLink.__ORG_MD2),
            FileContainer(TestMdLink.__ORG_MD3),
            FileContainer(TestMdLink.__ORG_MD3_CONT),
        ]

        fc_act = gen_md_anchor_all(mds)

        self.assertEqual(FileContainer(TestMdLink.__ANC_MD1).content, fc_act[0].content)
        self.assertEqual(
            FileContainer(TestMdLink.__ANC_MD2_SEQ).content, fc_act[1].content
        )
        self.assertEqual(
            FileContainer(TestMdLink.__ANC_MD3_SEQ).content, fc_act[2].content
        )
        self.assertEqual(
            FileContainer(TestMdLink.__ANC_MD3_CONT).content, fc_act[3].content
        )

    def test_gen_md_anchor_err1(self):
        try:
            fc_act = gen_md_anchor_all([FileContainer(TestMdLink.__ORG_MD1_ERR1)])
        except ValueError as e:
            self.assertEqual(
                "#### X\n skip level",
                e.args[0],
            )
        else:
            assert False

    def test_gen_md_section_db1(self):
        fc1 = FileContainer(TestMdLink.__ANC_MD1)
        db_act = gen_md_section_db([fc1])

        db_exp = [
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1",
                "full_anchor": "simple1_anchor.md#SS_1",
                "section": ["Simple1.1"],
                "excerpt": "\u30c7\u30fc\u30bf1\n",
            },
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1_1",
                "full_anchor": "simple1_anchor.md#SS_1_1",
                "section": ["Simple1.1", "Simple1.1 A"],
                "excerpt": "\u30c7\u30fc\u30bf1-1\n",
            },
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1_1_1",
                "full_anchor": "simple1_anchor.md#SS_1_1_1",
                "section": ["Simple1.1", "Simple1.1 A", "X"],
                "excerpt": "\n",
            },
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1_2",
                "full_anchor": "simple1_anchor.md#SS_1_2",
                "section": ["Simple1.1", "Simple1.1-2"],
                "excerpt": '### X <a id="SS_1_2_1"></a>\n',
            },
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1_2_1",
                "full_anchor": "simple1_anchor.md#SS_1_2_1",
                "section": ["Simple1.1", "Simple1.1-2", "X"],
                "excerpt": "\u5909\u63db\u30c6\u30b9\u30c8 [Simple1.1](---)\u3092\u53c2\u7167\u3002\n",
            },
        ]

        self.assertEqual(db_exp, db_act)

        fc2 = FileContainer(TestMdLink.__ANC_MD2)

        db_act = gen_md_section_db([fc2])

    def test_gen_md_section_db2(self):
        fc1 = FileContainer(TestMdLink.__ANC_MD1)
        fc2 = FileContainer(TestMdLink.__ANC_MD2)
        fc3 = FileContainer(TestMdLink.__ANC_MD3)

        db_act = gen_md_section_db([fc1, fc2, fc3])

        db_exp = [
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1",
                "full_anchor": "simple1_anchor.md#SS_1",
                "section": ["Simple1.1"],
                "excerpt": "\u30c7\u30fc\u30bf1\n",
            },
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1_1",
                "full_anchor": "simple1_anchor.md#SS_1_1",
                "section": ["Simple1.1", "Simple1.1 A"],
                "excerpt": "\u30c7\u30fc\u30bf1-1\n",
            },
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1_1_1",
                "full_anchor": "simple1_anchor.md#SS_1_1_1",
                "section": ["Simple1.1", "Simple1.1 A", "X"],
                "excerpt": "\n",
            },
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1_2",
                "full_anchor": "simple1_anchor.md#SS_1_2",
                "section": ["Simple1.1", "Simple1.1-2"],
                "excerpt": '### X <a id="SS_1_2_1"></a>\n',
            },
            {
                "filename": "simple1_anchor.md",
                "anchor": "SS_1_2_1",
                "full_anchor": "simple1_anchor.md#SS_1_2_1",
                "section": ["Simple1.1", "Simple1.1-2", "X"],
                "excerpt": "\u5909\u63db\u30c6\u30b9\u30c8 [Simple1.1](---)\u3092\u53c2\u7167\u3002\n",
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1",
                "full_anchor": "simple2_anchor.md#SS_1",
                "section": ["Simple2.1"],
                "excerpt": "\u30c7\u30fc\u30bf1\n",
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_1",
                "full_anchor": "simple2_anchor.md#SS_1_1",
                "section": ["Simple2.1", "Simple2.1-1"],
                "excerpt": "\u30c7\u30fc\u30bf1-1\n",
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_1_1",
                "full_anchor": "simple2_anchor.md#SS_1_1_1",
                "section": ["Simple2.1", "Simple2.1-1", "Simple2.1-1-1"],
                "excerpt": "\u30c7\u30fc\u30bf1-1-1\n",
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_1_2",
                "full_anchor": "simple2_anchor.md#SS_1_1_2",
                "section": ["Simple2.1", "Simple2.1-1", "Simple2.1-1-2"],
                "excerpt": "\u30c7\u30fc\u30bf1-1-2\n",
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_1_3",
                "full_anchor": "simple2_anchor.md#SS_1_1_3",
                "section": ["Simple2.1", "Simple2.1-1", "Simple2.1-1-3"],
                "excerpt": "\u30c7\u30fc\u30bf1-1-3\n",
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_2",
                "full_anchor": "simple2_anchor.md#SS_1_2",
                "section": ["Simple2.1", "Simple2.1-2"],
                "excerpt": '### Simple2.1-2-1 <a id="SS_1_2_1"></a>\n',
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_2_1",
                "full_anchor": "simple2_anchor.md#SS_1_2_1",
                "section": ["Simple2.1", "Simple2.1-2", "Simple2.1-2-1"],
                "excerpt": '#### Simple2.1-2-1-1 <a id="SS_1_2_1_1"></a>\n',
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_2_1_1",
                "full_anchor": "simple2_anchor.md#SS_1_2_1_1",
                "section": [
                    "Simple2.1",
                    "Simple2.1-2",
                    "Simple2.1-2-1",
                    "Simple2.1-2-1-1",
                ],
                "excerpt": '### Simple2.1-2-2 <a id="SS_1_2_2"></a>\n',
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_2_2",
                "full_anchor": "simple2_anchor.md#SS_1_2_2",
                "section": ["Simple2.1", "Simple2.1-2", "Simple2.1-2-2"],
                "excerpt": '#### Simple2.1-2-2-1 <a id="SS_1_2_2_1"></a>\n',
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_2_2_1",
                "full_anchor": "simple2_anchor.md#SS_1_2_2_1",
                "section": [
                    "Simple2.1",
                    "Simple2.1-2",
                    "Simple2.1-2-2",
                    "Simple2.1-2-2-1",
                ],
                "excerpt": '#### Simple2.1-2-2-2 <a id="SS_1_2_2_2"></a>\n',
            },
            {
                "filename": "simple2_anchor.md",
                "anchor": "SS_1_2_2_2",
                "full_anchor": "simple2_anchor.md#SS_1_2_2_2",
                "section": [
                    "Simple2.1",
                    "Simple2.1-2",
                    "Simple2.1-2-2",
                    "Simple2.1-2-2-2",
                ],
                "excerpt": "\n",
            },
            {
                "filename": "simple3_anchor.md",
                "anchor": "SS_1",
                "full_anchor": "simple3_anchor.md#SS_1",
                "section": ["Simple3.1"],
                "excerpt": "\u30c7\u30fc\u30bf1\n",
            },
            {
                "filename": "simple3_anchor.md",
                "anchor": "SS_1_1",
                "full_anchor": "simple3_anchor.md#SS_1_1",
                "section": ["Simple3.1", "Simple3.1-1"],
                "excerpt": "\u30c7\u30fc\u30bf1-1\n",
            },
            {
                "filename": "simple3_anchor.md",
                "anchor": "SS_1_1_1",
                "full_anchor": "simple3_anchor.md#SS_1_1_1",
                "section": ["Simple3.1", "Simple3.1-1", "X"],
                "excerpt": "\u30c7\u30fc\u30bf1-1-1\n",
            },
        ]

        self.assertEqual(db_exp, db_act)

    def test_gen_md_section_db3(self):
        fc1 = FileContainer(TestMdLink.__ANC_MD1)
        fc2 = FileContainer(TestMdLink.__ANC_MD2)
        fc3 = FileContainer(TestMdLink.__ANC_MD3)

        db_act = gen_md_section_db([fc1, fc2, fc3])

        db_exp = load_db(TestMdLink.__EXP_JSON)

        self.assertEqual(db_exp, db_act)

        store_db(TestMdLink.__ACT_JSON, db_act)

        self.assertEqual(
            FileContainer(self.__EXP_JSON).content,
            FileContainer(TestMdLink.__ACT_JSON).content,
        )

    def test_gen_md_index_md(self):
        db_exp = load_db(TestMdLink.__EXP_JSON)

        index_content_act = gen_md_index_md(db_exp, "# インデックス\n", [], [], False)

        index_content_exp = FileContainer(TestMdLink.__EXP_INDEX_MD).content

        self.assertEqual(index_content_exp, index_content_act)

    def test_SectionDict(self):
        db_exp = load_db(TestMdLink.__EXP_JSON)

        sd = SectionDict(db_exp)

        self.assertEqual(
            sd.section2anchor("Simple1.1"), sd.section2anchor("|Simple1.1")
        )

        anchor_section = [
            ("simple1_anchor.md#SS_1", "Simple1.1"),
            ("simple1_anchor.md#SS_1_1", "Simple1.1 A"),
            ("simple2_anchor.md#SS_1_2_2_2", "Simple2.1-2-2-2"),
        ]
        for anchor, sec in anchor_section:
            self.assertEqual(anchor, sd.section2anchor(sec))

        anchor_section = [
            ("simple1_anchor.md#SS_1_1", "Simple1.1 A"),
            ("simple1_anchor.md#SS_1_1_1", "Simple1.1 A|X"),
            (
                "simple2_anchor.md#SS_1_2_2_2",
                "Simple2.1-2|Simple2.1-2-2|Simple2.1-2-2-2",
            ),
            ("simple2_anchor.md#SS_1_2_2_2", "Simple2.1-2-2|Simple2.1-2-2-2"),
            ("simple2_anchor.md#SS_1_2_2_2", "Simple2.1-2-2-2"),
        ]
        for anchor, sec in anchor_section:
            self.assertEqual(anchor, sd.section2anchor(sec))

        try:
            sd.section2anchor("X")
        except ValueError as e:
            self.assertEqual(
                "X has many candidates\n"
                "\tsimple1_anchor.md#SS_1_1_1\n"
                "\tsimple1_anchor.md#SS_1_2_1\n"
                "\tsimple3_anchor.md#SS_1_1_1",
                e.args[0],
            )
        else:
            assert False

    def test_sub_ref(self):
        content_org = [
            "一つ変換[Simple1.1 A](---)を参照\n。",
            "この行は変換しない。\n",
            "2つ変換[Simple1.1 A|X](---)、[Simple2.1-2-2|Simple2.1-2-2-2](---)。\n",
        ]

        content_exp = [
            "一つ変換[Simple1.1 A](simple1_anchor.md#SS_1_1)を参照\n。",
            "この行は変換しない。\n",
            "2つ変換[X](simple1_anchor.md#SS_1_1_1)、"
            "[Simple2.1-2-2-2](simple2_anchor.md#SS_1_2_2_2)。\n",
        ]
        db_exp = load_db(TestMdLink.__EXP_JSON)

        sd = SectionDict(db_exp)

        content_act = sd.resolve_ref_in_content(content_org)

        self.assertNotEqual(content_org, content_exp)
        self.assertEqual(content_act, content_exp)

    def test_integrate_mds(self):
        sd = SectionDict(load_db(TestMdLink.__EXP_JSON))

        for org, res in [
            (TestMdLink.__ORG_MD1, TestMdLink.__RES_MD1),
            (TestMdLink.__ORG_MD2, TestMdLink.__RES_MD2),
            (TestMdLink.__ORG_MD3, TestMdLink.__RES_MD3),
        ]:
            md_org = FileContainer(org)
            md_anchor = gen_md_anchor_all([md_org])
            md_resolved = sd.resolve_ref(md_anchor[0])

            self.assertEqual(FileContainer(res).content, md_resolved.content)

    def test_change_md_link_to_html(self):
        org = [
            "&emsp; [Simple3.1](simple3_anchor.md#simple3.1)",
            "X [Simple1.1](simple1_anchor.md#simple1.1) ",
            "X [Simple1.1](simple1_anchor.md#simple1.1) "
            "Y [Simple1.1 A](simple1_anchor.md#simple1.1.1)",
        ]

        exp = [
            "&emsp; [Simple3.1](simple3_anchor.html#simple3.1)",
            "X [Simple1.1](simple1_anchor.html#simple1.1) ",
            "X [Simple1.1](simple1_anchor.html#simple1.1) "
            "Y [Simple1.1 A](simple1_anchor.html#simple1.1.1)",
        ]

        self.assertEqual(exp, change_link_ext("md", "html", org))
