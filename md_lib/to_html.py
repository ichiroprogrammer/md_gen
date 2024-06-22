import re
import pprint
from os import path

from md_lib.file_container import FileContainer
from md_lib.link_ref import change_link_ext

_LINK_MD_TO_HTML = re.compile(r'("\w+\.)md([#S_0-9]*")')
_STYLE_END = re.compile(r"</style>")
TABLE_START = re.compile(r"table {$")
TABLE_END = re.compile(r"}$")

_STYLE_CSS = """
    body {
        margin: 0 auto;
        max-width: none;
        width: 1000px;
        padding-left: 50px;
        padding-right: 50px;
        padding-top: 50px;
        padding-bottom: 50px;
        hyphens: auto;
        overflow-wrap: break-word;
        text-rendering: optimizeLegibility;
        font-kerning: normal;
    }

    table {
        border-collapse: collapse;
    }

    table, th, td {
        border: 2px solid black;
    }

    header {
        margin-bottom: 4em;
        text-align: center;
        color: white;
        background-color: lightblue;
    }

    h1:not(:first-of-type) {
        page-break-before: always;
    }
"""


def adjust_html(fc: FileContainer) -> FileContainer:  # fc for html
    new_content = []

    deleting = False
    for line in fc.content:
        if _STYLE_END.search(line):
            new_content += [line_css + "\n" for line_css in _STYLE_CSS.split("\n")]

        if _LINK_MD_TO_HTML.search(line):
            line = _LINK_MD_TO_HTML.sub(r"\1html\2", line)

        if TABLE_START.search(line):
            deleting = True

        if deleting and TABLE_END.search(line):
            line = None
            deleting = False

        if not deleting and line:
            new_content.append(line)

    return FileContainer(fc.filename, new_content)
