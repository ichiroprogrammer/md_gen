import unittest
import os

from md_lib.file_container import FileContainer


class TestFileContainer(unittest.TestCase):
    __ORG_FILE = "test/data/simple2.md"
    __COPY_FILE = f"{__ORG_FILE}.cp"

    def setUp(self):
        if os.path.exists(TestFileContainer.__COPY_FILE):
            os.remove(TestFileContainer.__COPY_FILE)

    def tearDown(self):
        if os.path.exists(TestFileContainer.__COPY_FILE):
            os.remove(TestFileContainer.__COPY_FILE)

    def test_init(self):
        test_md = [
            "# Simple2.1\n",
            "データ1\n",
            "\n",
            "## Simple2.1-1\n",
            "データ1-1\n",
            "\n",
            "### Simple2.1-1-1\n",
            "データ1-1-1\n",
            "\n",
            "### Simple2.1-1-2\n",
            "データ1-1-2\n",
            "\n",
            "### Simple2.1-1-3\n",
            "データ1-1-3\n",
            "\n",
            "## Simple2.1-2\n",
            "### Simple2.1-2-1\n",
            "#### Simple2.1-2-1-1\n",
            "### Simple2.1-2-2\n",
            "#### Simple2.1-2-2-1\n",
            "#### Simple2.1-2-2-2\n",
            "\n",
            "\n",
        ]

        fc = FileContainer(TestFileContainer.__ORG_FILE)

        self.assertEqual(test_md, fc.content)

    def test_cd(self):
        fc = FileContainer(TestFileContainer.__ORG_FILE)
        fc.cd("test2/data2")

        self.assertEqual(fc.filename, "test2/data2/simple2.md")

    def test_save(self):
        fc = FileContainer(TestFileContainer.__ORG_FILE)

        fc2 = FileContainer(TestFileContainer.__COPY_FILE, fc.content)
        self.assertEqual(fc2.content, fc.content)

        fc2.save()

        fc3 = FileContainer(TestFileContainer.__COPY_FILE)

        self.assertEqual(fc2, fc3)
