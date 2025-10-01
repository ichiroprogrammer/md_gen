import unittest
from pprint import pprint

from md_lib.file_container import FileContainer
from md_lib.code_ref import (
    ref_srcs,
    inject_code,
    CodeChunkDict,
    SampleCode,
    gen_sample_file_section,
    ref_srcs_by_dict,
)


class TestCodeRef(unittest.TestCase):
    __ORG_MD = "test/data/code_ref_no_code.md"
    __EXP_MD = "test/data/code_ref.md"
    __INC_TEST_MD = "test/data/include_test.md"

    def test_ref_srcs(self):
        fc = FileContainer(TestCodeRef.__INC_TEST_MD)

        # ref_srcsの仕様変更
        #   ソースコードのインクルードファイルは、mdファイルの生成に無関係なため、
        #   mdファイル内のソースコードのインクルードファイルを結果に含めない。
        #
        #       exp = [
        #           "test/data/header_1.h",
        #           "test/data/header_1_1.h",
        #           "test/data/header_2.h",
        #           "test/data/src_3.cpp",
        #           "test/data/src_4.cpp",
        #           "test/data_pu/rectangle_square.png",
        #           "test/vim_config/xxx.vim",
        #       ]
        exp = [
            "test/data/src_3.cpp",
            "test/data/src_4.cpp",
            "test/data_pu/rectangle_square.png",
            "test/vim_config/xxx.vim",
        ]

        act = ref_srcs(fc)

        self.assertEqual(exp, act)

    def test_inject_code(self):
        fc_org = FileContainer(TestCodeRef.__ORG_MD)

        injected_content = inject_code(fc_org)

        fc_exp = FileContainer(TestCodeRef.__EXP_MD)

        self.assertEqual(injected_content, fc_exp.content)

    def test_gen_code_chunk(self):
        code_dict = CodeChunkDict()

        #
        chunk = code_dict.get_code_chunk(("test/data/src_1.cpp", "0:0"))

        self.assertEqual(chunk.filename, "test/data/src_1.cpp")
        self.assertEqual(chunk.index, "0:0")
        self.assertEqual(chunk.line_num, 3)
        expect = [
            "\n",
            "    int32_t* a = 0;        // NG   オールドスタイル\n",
            "    int32_t* b = NULL;     // NG   C90の書き方\n",
            "    int32_t* c = nullptr;  // OK   C++11\n",
            "\n",
        ]
        self.assertEqual(chunk.code_chunk, expect)

        #
        chunk = code_dict.get_code_chunk(("test/data/src_1.cpp", "0:1"))

        self.assertEqual(chunk.filename, "test/data/src_1.cpp")
        self.assertEqual(chunk.index, "0:1")
        self.assertEqual(chunk.line_num, 11)
        expect = ["\n", "    IGNORE_UNUSED_VAR(a);\n", "    // ...\n"]
        self.assertEqual(chunk.code_chunk, expect)

        #
        chunk = code_dict.get_code_chunk(("test/data/src_1.cpp", "1:0"))

        self.assertEqual(chunk.filename, "test/data/src_1.cpp")
        self.assertEqual(chunk.index, "1:0")
        self.assertEqual(chunk.line_num, 24)
        expect = ["\n", "    bool b = false;\n", "\n", "\n", "    bool c;\n"]
        self.assertEqual(chunk.code_chunk, expect)

        #
        chunk = code_dict.get_code_chunk(("test/data/src_2.cpp", "0:0"))

        self.assertEqual(chunk.filename, "test/data/src_2.cpp")
        self.assertEqual(chunk.index, "0:0")
        self.assertEqual(chunk.line_num, 2)
        expect = ["\n", "void g(int32_t* ptr0, int32_t* ptr1)\n", "{\n", "}\n", "\n"]
        self.assertEqual(chunk.code_chunk, expect)

    def test_gen_sample_file_section(self):
        fc = FileContainer(TestCodeRef.__INC_TEST_MD)

        files_act = ref_srcs_by_dict([fc])

        files_exp = {
            "makefile": [],
            "vim": [SampleCode("vim_config/xxx.vim", "test/vim_config/xxx.vim")],
            "cpp": [],
            "python": [],
            "etc": [],
        }

        self.assertEqual(files_exp, files_act)

        files_exp["makefile"].extend(
            [
                SampleCode("data/fake.mk", "test/data/fake.mk"),
                SampleCode("data/Makefile", "test/data/Makefile"),
            ]
        ),

        content = gen_sample_file_section(files_exp)

        fc = FileContainer("test/data/sample_sec.md")

        self.assertEqual(content, fc.content)
