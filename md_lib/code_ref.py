import re
import pprint
from os import path

from md_lib.file_container import FileContainer, related_path_in_md
from md_lib.png_ref import get_png_in_link


class CodeRefSyntax:
    REF_BEGIN = re.compile(
        r"^(?P<space> *)[^@ ]+ @@@ (?P<src>[\w/._\-]+)[ ]*#(?P<index>\d+:\d+(:\d+)?) "
        "begin *(?P<offset>-?\d)? *(?P<cr>-?\d)?\n"
    )

    CODE_BEGIN = re.compile(
        r"^((# )|(?P<space> *))(// )?@@@ sample begin (?P<index>\d+:\d+(:\d+)?)\n"
    )
    CODE_END = re.compile(r"@@@ sample end\n")

    CODE_IGNORE_BEGIN = re.compile(r"@@@ ignore begin\n")
    CODE_IGNORE_END = re.compile("^(?P<space> *)[^ ]* ?@@@ ignore end\n")

    CODE_DELETE = re.compile("(@@@ delete)|(clang-format (on)|(off))\n")

    # コードブロックの行番号表示
    CODE_BLOCK = re.compile("^```")  # ```のみに対応
    CODE_BLOCK_LINENO = re.compile("^ *@@@  *lineno")


def _gen_file_content(filename: str, sort: str):
    fc = FileContainer(filename)
    indent = " " * 8

    return (
        [f"```{sort}\n"]
        + [f"{indent}{i:>3} {line}" for i, line in enumerate(fc.content, 1)]
        + [f"```\n"]
        + ["\n"]
    )


class SampleCode:
    def __init__(self, section_name, file_path):
        self._section_name = section_name
        self._file_path = file_path

    @property
    def section_name(self):
        return self._section_name

    @property
    def file_path(self):
        return self._file_path

    def __str__(self):
        return f"{self.section_name}:{self.file_path}"

    def __eq__(self, other):
        if isinstance(other, SampleCode):
            return (
                self.section_name == other.section_name
                and self.file_path == other.file_path
            )
        return False

    def __hash__(self):
        return hash((self.section_name, self.file_path))

    def __lt__(self, other):
        if isinstance(other, SampleCode):
            if self.section_name == other.section_name:
                return self.file_path < other.file_path
            else:
                return self.section_name < other.section_name

        return NotImplemented


def _gen_default_section(sample_codes: [SampleCode], section_name, code_name):
    content = [f"## {section_name}\n"]

    for sc in sample_codes:
        sc_name = sc.section_name.replace("__", r"\_\_")
        content.append(f"### {sc_name}\n")
        content += _gen_file_content(sc.file_path, code_name)

    return content


def gen_sample_file_section(to_gen: dict) -> [str]:
    ret = ["# Sample Code\n"]

    for sort, sample_codes in to_gen.items():
        if len(sample_codes) == 0:
            continue

        if sort == "makefile":
            ret += _gen_default_section(sample_codes, "build code", "makefile")
        elif sort == "plant_uml":
            ret += _gen_default_section(sample_codes, "plant uml", "")
        elif sort == "cpp":
            ret += _gen_default_section(sample_codes, "C++", "cpp")
        elif sort == "bash":
            ret += _gen_default_section(sample_codes, "bash", "bash")
        elif sort == "python":
            ret += _gen_default_section(sample_codes, "python", "python")
        elif sort == "vim":
            ret += _gen_default_section(sample_codes, "vim", "vim")
        elif sort == "etc":
            if len(sample_codes) != 0:
                ret += _gen_default_section(sample_codes, "etc", "")
        else:
            pass

    ret += ["\n", "\n"]

    return ret


_CPP_INCLUDE = re.compile(r' *# *include *"(?P<header>\w+\.\w+)"')


def _get_ref_headers(src: str):
    fc = FileContainer(src)
    headers = []

    for line in fc.content:
        match_inc = _CPP_INCLUDE.match(line)
        if match_inc:
            header = match_inc.groupdict()["header"]
            header = _find_header(f"{path.dirname(src)}/{header}")

            if not header in headers:
                headers.append(header)
                headers += _get_ref_headers(header)

    return headers


def _find_header(header: str):
    if path.isfile(header):
        return header

    split_path = path.split(header)

    header = f"{split_path[0]}/../h/{split_path[1]}"

    if path.isfile(header):
        return header

    raise (ValueError(f"{header} not found"))


_REF_FILE_RE = re.compile(r"\"\[(?P<name>[^\"\]]+)\]\(---\)\"")
# " <-このようにしないと上の正規表現の影響でシンタックスハイライトが崩れる。


def _link_file(md_file_path: str, line: str):
    if match_file := _REF_FILE_RE.search(line):
        name = match_file.groupdict()["name"]
        src = related_path_in_md(md_file_path, name)
        if path.exists(src):
            return SampleCode(name, src)

        raise (ValueError(f"{src} not found"))

    return None


def _ref_srcs_row(fc: FileContainer, png_to_pu: bool) -> [str]:
    refs = []

    for line in fc.content:
        if match_beg := CodeRefSyntax.REF_BEGIN.search(line):
            src = related_path_in_md(fc.filename, match_beg.groupdict()["src"])
            refs.append(src)
            # refs += _get_ref_headers(src) # ref_srcsの仕様変更
        elif png := get_png_in_link(fc.filename, line):
            pu = png.replace("png", "pu")

            if path.exists(pu):
                if png_to_pu:
                    refs.append(pu)
                else:
                    refs.append(png)
        elif sample_code := _link_file(fc.filename, line):
            refs.append(sample_code.file_path)

    return refs


def ref_srcs(fc: FileContainer) -> [str]:
    refs = _ref_srcs_row(fc, False)

    return sorted(set(refs))


def ref_srcs_by_dict(fcs: [FileContainer]) -> dict:
    refs = []

    for fc in fcs:
        for line in fc.content:
            if file := _link_file(fc.filename, line):
                refs.append(file)

    refs = sorted(set(refs))

    mk_re = re.compile(r".*[Mm]akefile$")
    mk_re2 = re.compile(r".*\.mk")
    cpp_re = re.compile(r"\.(cpp|h)$")
    py_re = re.compile(r"\.py$")
    vim_re = re.compile(r".*/*vim_config/.*")

    ret = {
        "makefile": [],
        "vim": [],
        "cpp": [],
        "python": [],
        "etc": [],
    }

    for r in refs:
        file_path = r.file_path
        if vim_re.search(file_path):
            ret["vim"].append(r)
        elif mk_re.search(file_path) or mk_re2.search(file_path):
            ret["makefile"].append(r)
        elif cpp_re.search(file_path):
            ret["cpp"].append(r)
        elif py_re.search(file_path):
            ret["python"].append(r)
        else:
            ret["etc"].append(r)

    return ret


class CodeChunkDict:
    def __init__(self):
        self.__dict = {}

    def get_code_chunk(self, filename_index):  # (filename, index)
        if code_chunk := self.__dict.get(filename_index):
            return code_chunk

        fc = FileContainer(filename_index[0])
        chunks = self._gen_code_chunk(fc)

        for chunk in chunks:
            self.__dict[(chunk.filename, chunk.index)] = chunk

        if code_chunk := self.__dict.get(filename_index):
            return code_chunk

        # pprint.pprint(self.__dict)
        raise ValueError(f"unknown {filename_index[0]}-{filename_index[1]}")

    def _gen_code_chunk(self, file_container):
        ret = []

        in_code = False
        ref_code = []
        index = line_num = None
        ref_code_indent = 0

        for i, line in enumerate(file_container.content):
            if in_code:
                if CodeRefSyntax.CODE_END.search(line):
                    ret.append(
                        CodeChunk(
                            file_container.filename,
                            ref_code_indent,
                            index,
                            line_num,
                            self._delete_ignore_code(ref_code),
                        )
                    )
                    in_code = False
                    ref_code = []
                else:
                    ref_code.append(line)

            else:
                if match_beg := CodeRefSyntax.CODE_BEGIN.search(line):
                    in_code = True
                    index = match_beg.groupdict()["index"]

                    if match_beg.groupdict()["space"]:
                        ref_code_indent = int(len(match_beg.groupdict()["space"]) / 4)
                    else:
                        ref_code_indent = 0

                    line_num = i + 1

        return ret

    def _delete_ignore_code(self, content):
        ret = []
        in_ignore = False

        for line in content:
            if in_ignore:
                if match_end := CodeRefSyntax.CODE_IGNORE_END.search(line):
                    in_ignore = False
                    line = f"{match_end.groupdict()['space']}...\n"
                    ret.append(line)
            else:
                if CodeRefSyntax.CODE_IGNORE_BEGIN.search(line):
                    in_ignore = True
                else:
                    ret.append(line)

        return [line for line in ret if not CodeRefSyntax.CODE_DELETE.search(line)]


class CodeChunk:
    def __init__(self, filename, indent, index, line_num, code_chunk):
        self.__filename = filename
        self.__indent = indent  # int comment indent
        self.__index = index  # str(\d:\d)
        self.__line_num = line_num  # int
        self.__code_chunk = code_chunk  # [str, ... ]

    def __repr__(self):
        return f"{self.__filename}-{self.__index}-{self.__line_num}-{self.__code_chunk}"

    def __str__(self):
        return f"{self.__filename}-{self.__index}-{self.__line_num}-{self.__code_chunk}"

    @property
    def filename(self):
        pass

    @filename.getter
    def filename(self):
        return self.__filename

    @property
    def indent(self):
        pass

    @indent.getter
    def indent(self):
        return self.__indent

    @property
    def index(self):
        pass

    @index.getter
    def index(self):
        return self.__index

    @property
    def line_num(self):
        pass

    @line_num.getter
    def line_num(self):
        return self.__line_num

    @property
    def code_chunk(self):
        pass

    @code_chunk.getter
    def code_chunk(self):
        return self.__code_chunk


def _adjust_indent(content, ref_code_indent, indent, offset, cr):  # offset intマイナス or 0
    if cr > 0:
        content = ["\n" for i in range(0, cr)] + content

    indent_str = "    "

    if indent + offset < 0:
        del_count = (indent + offset + ref_code_indent) * 4
        return [line[del_count:] if len(line) > del_count else line for line in content]
    else:
        indent_str = indent_str * (indent + offset)
        return [indent_str + line if line != "\n" else line for line in content]


def inject_code(fc: FileContainer):
    after_index = re.compile(" *#\d+:\d+(:\d+)? begin *(-?\d)? *(\d)?")  # REF_BEGIN参照
    new_content = []
    code_dict = CodeChunkDict()

    just_injected = False

    for line in fc.content:
        if match_beg := CodeRefSyntax.REF_BEGIN.search(line):
            gd = match_beg.groupdict()
            src = related_path_in_md(fc.filename, gd["src"])
            chunk = code_dict.get_code_chunk((src, gd["index"]))

            indent = int(len(gd["space"]) / 4)

            offset = int(gd["offset"]) if gd["offset"] else 0

            cr = int(gd["cr"]) if gd["cr"] else 0  # cr == -1ならばソースコード表示しない

            if ((not just_injected) or src != last_src) and cr >= 0:
                new_content.append(
                    after_index.sub(f" {chunk.line_num}", line).replace("@@@", "")
                )

            new_content += _adjust_indent(
                chunk.code_chunk, chunk.indent, indent, offset, cr
            )

            last_src = src
            just_injected = True
        else:
            new_content.append(line)
            just_injected = False

    return _add_number_to_code_block(new_content)


def _add_number_to_code_block(content):
    add_num = False
    line_num = 0
    in_code_block = False
    new_content = []

    for line in content:
        if CodeRefSyntax.CODE_BLOCK.search(line):
            if in_code_block:
                in_code_block = False
            else:
                in_code_block = True
                line_num = 0
                add_num = False

        if in_code_block:
            if line_num == 1 and CodeRefSyntax.CODE_BLOCK_LINENO.search(line):
                add_num = True
                continue

            if add_num and line_num != 0:
                line = "{0:3} {1}".format(line_num, line)
            line_num += 1

        new_content.append(line)

    return new_content
