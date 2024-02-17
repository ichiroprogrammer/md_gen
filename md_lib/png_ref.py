import re
import base64
import pprint
from os import path

from md_lib.file_container import FileContainer, related_path_in_md


_REF_PU_PNG = re.compile(r"^!\[[^\]]+\]\((?P<png>[^\)]+\.png)\)\n")


def get_png_in_link(md_file_path: str, line: str) -> str:
    if match_png := _REF_PU_PNG.search(line):
        return related_path_in_md(md_file_path, match_png.groupdict()["png"])

    return None


def _image2base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def change_png_link_to_base64(fc: FileContainer) -> FileContainer:
    new_content = []

    for line in fc.content:
        if match_png := _REF_PU_PNG.match(line):
            png = related_path_in_md(fc.filename, match_png.groupdict()["png"])
            base64 = _image2base64(png)

            line = f'<p><img src="data:image/png;base64,{base64}" /></p>\n'

        new_content.append(line)

    return FileContainer(fc.filename, new_content)
