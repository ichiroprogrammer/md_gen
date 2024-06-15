import re
import os
import base64
import pprint
from os import path

from md_lib.file_container import FileContainer, related_path_in_md


_REF_PU_PNG = re.compile(r"^!\[[^\]]+\]\((?P<png>[^\)]+\.png)\)\n")
_REF_PU_FILE = re.compile("<!--\s*pu:(?P<pu>[^>]+)\s*-->")


def get_png_in_link(md_file_path: str, line: str) -> str:
    if match_png := _REF_PU_PNG.search(line):
        return related_path_in_md(md_file_path, match_png.groupdict()["png"])

    return None


def _image2base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def _gen_pu_file(png):
    base_name, tmp = os.path.splitext(png)
    pu_file = base_name + ".pu"

    if os.path.exists(pu_file):
        return pu_file
    else:
        return None


def get_pu_content(line):
    pu_code_chunk = []
    if match_png := _REF_PU_FILE.match(line):
        pu_file = match_png.groupdict()["pu"]
        pu_code_chunk.append(f"```{pu_file}\n")
        pu_content = FileContainer(pu_file)
        pu_code_chunk.extend(pu_content.content)
        pu_code_chunk.append("```\n")
        return pu_code_chunk
    else:
        return None


def change_png_link_to_base64(fc: FileContainer) -> FileContainer:
    new_content = []

    for line in fc.content:
        if match_png := _REF_PU_PNG.match(line):
            png = related_path_in_md(fc.filename, match_png.groupdict()["png"])
            pu_file = _gen_pu_file(png)

            if pu_file:
                line = f"<!-- pu:{pu_file}-->"
            else:
                dir = os.path.dirname(png)
                line = f"<!-- pu:{dir}/fake.pu-->"

            base64 = _image2base64(png)
            line += f'<p><img src="data:image/png;base64,{base64}" /></p>\n'

        new_content.append(line)

    return FileContainer(fc.filename, new_content)
