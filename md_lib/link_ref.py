from collections import defaultdict
from os import path
import json
import re
import unicodedata

import pprint

from md_lib.file_container import FileContainer
from md_lib.png_ref import change_png_link_to_base64

# あえて2つのマッチを作ることによってセクション開始文字列の不正を防ぐ
_MD_SECTION_SIMPLE_RE = re.compile(r"#+")
_MD_SECTION_ROW_RE = re.compile(
    r"^(?P<sharp>#+)(\s*)(?P<sec_num>[0-9.]+)?(\s+)(?P<name>.+)\n"
)
_MD_SECTION_ANCHOR_RE = re.compile(
    r'^(?P<sharp>#+) (?P<name>.+) <a id="(?P<anchor>.+)"></a>\n'
)

_MD_UMCOMPLETED_REF_RE = re.compile(r"\[(?P<name>[^\]]+)\]\(---\)")
_MD_UMCOMPLETED_REF_EXCEPT_RE = re.compile(r"^ {8,}[\"\[]")  # example/*.mdのために必要
_MD_UMCOMPLETED_REF2_RE = re.compile(r"\[(?P<name>[^\]]+)\]\(~~~\)")  # リンク先がない場合にも対応
_MD_SECTION_SEP = "|"

_MD_INDEX_INJECTION_RE = re.compile(r"^<!-- index (?P<first>\d+)-(?P<exclude>\d+) -->")


def inject_index(md: FileContainer, content: [str]) -> [str]:
    ret = []

    for line in content:
        if match_sec := _MD_INDEX_INJECTION_RE.match(line):
            exclude = match_sec.groupdict()["exclude"]
            first = match_sec.groupdict()["first"]
            small_db = gen_md_section_db([md])
            index = gen_md_index_md(small_db, [], [], [f".*.md:{exclude}"], False)
            ret.extend(index[int(first) :])

        else:
            ret.append(line)

    return ret


def add_sec_num(content: [str]) -> [str]:
    ret = []

    for line in content:
        if match_sec := _MD_SECTION_ANCHOR_RE.match(line):
            name = match_sec.groupdict()["name"]
            sec_num = _gen_sec_num_from_anchor(match_sec.groupdict()["anchor"])
            pos = line.find(name)
            ret.append(line[:pos] + f"{sec_num} " + line[pos:])
        else:
            ret.append(line)

    return ret


def change_link_ext(from_ext: str, to_ext, content: [str]) -> [str]:
    completed_ref = re.compile(
        rf"(\[[^\]]+\]\([^\]\[\(\)]+\.)({from_ext})([^\]\[\(\)]*\))"
    )

    return [completed_ref.sub(rf"\1{to_ext}\3", line) for line in content]


def del_filename_in_link(content: [str]) -> [str]:
    file_in_link_ref = re.compile(r"(\[[^\]]+\]\()([^\]\[\(\)#]+)(#[^\]\[\(\)#]*\))")

    return [file_in_link_ref.sub(rf"\1\3", line) for line in content]


_SEC_NUM_PREFIX = "SS_"


def _gen_sec_num_from_anchor(anctor: str):
    return anctor.replace(_SEC_NUM_PREFIX, "").replace("_", ".")


def _gen_anchor_from_sec(section: [int]) -> str:
    ret = _SEC_NUM_PREFIX + str(section[0])
    section_after_level2 = section[1:-1]

    for num in section_after_level2:
        if not num:
            break

        ret += f"_{num}"

    return ret


def _section_level(sharps: str):  # "#の数がセクションレベル。1つのみがセクションレベル0
    sec_level = len(sharps) - 1
    assert sec_level >= 0

    return sec_level


def _add_anchor_to_line(section: [int], line: str) -> ([int], str):
    match_sec = _MD_SECTION_ROW_RE.match(line)
    sharp = match_sec.groupdict()["sharp"]
    name = match_sec.groupdict()["name"]

    if name.isspace():
        raise ValueError(f"{line} shall have a string")

    if _MD_SECTION_SEP in name:
        raise ValueError(f"{name} includes '{_MD_SECTION_SEP}'")

    sec_level = _section_level(sharp)

    if sec_level > 0 and section[sec_level - 1] == 0:
        raise ValueError(f"{line} skip level")

    section = [
        s if i <= sec_level else 0 for i, s in enumerate(section)
    ]  # sec_levelの後ろを0
    section[sec_level] += 1

    anchor = _gen_anchor_from_sec(section)

    return section, f'{sharp} {name} <a id="{anchor}"></a>\n'


def gen_md_anchor_all(mds: [FileContainer]) -> [FileContainer]:
    section = [0] * 10
    ret = []

    for md in mds:
        new_content = [f"<!-- {md.filename} -->\n"]
        prev_line = "\n"

        for index, line in enumerate(md.content):
            if _MD_SECTION_SIMPLE_RE.match(line):
                if not prev_line.isspace() and not _MD_SECTION_SIMPLE_RE.match(
                    prev_line
                ):
                    raise ValueError(
                        f"{md.filename}:{index} before {line} shall be space"
                    )

                section, line = _add_anchor_to_line(section, line)

            new_content.append(line)
            prev_line = line

        ret.append(FileContainer(md.filename, new_content))

    return ret


def _get_section_and_anchor(section, line):
    match_sec = _MD_SECTION_ANCHOR_RE.match(line)
    sharp = match_sec.groupdict()["sharp"]
    name = match_sec.groupdict()["name"]
    anchor = match_sec.groupdict()["anchor"]

    section = section[0 : _section_level(sharp)]

    if _MD_SECTION_SEP in name:
        raise ValueError(f"{name} includes '{_MD_SECTION_SEP}'")

    section.append(name)

    return section, anchor


def _gen_md_section_db_each(md: FileContainer, section) -> list:
    db = []

    prev_line = ""

    for curr_line in md.content:
        if _MD_SECTION_SIMPLE_RE.match(prev_line):
            section, anchor = _get_section_and_anchor(section, prev_line)

            filename = path.basename(md.filename)

            db.append(
                {
                    "filename": filename,
                    "anchor": anchor,
                    "full_anchor": filename + "#" + anchor,
                    "section": section,
                    "excerpt": curr_line,
                }
            )

        prev_line = curr_line
        # mdの最後の2行は空行であるので、セクションのチェック漏れはない

    return section, db


def gen_md_section_db(mds: [FileContainer]) -> list:
    section = []
    ret = []

    for md in mds:
        section, db = _gen_md_section_db_each(md, section)
        ret += db

    return ret


def store_db(filename: str, db: list):
    with open(filename, "w") as f:
        json.dump(db, f, indent=4)


def load_db(filename: str) -> list:
    with open(filename) as f:
        db = json.load(f)

    return db


def _gen_one_line(
    full_anchor: str, sec: list, sec_num_str: str, excerpt_str: str
) -> str:
    sec_name = sec[-1]
    head = "&emsp;" * len(sec)

    # 行末2spaceは改行のため必要
    return f"{head} {sec_num_str}[{sec_name}]({full_anchor}){excerpt_str}  \n"


def _gen_exc_re(exclude_str):
    filename, sec_num = exclude_str.split(":")

    sec_rexp = _SEC_NUM_PREFIX + r"\d+" + (int(sec_num) * r"_\d+")

    return re.compile(filename + "#" + sec_rexp)


def _with_excerpt(excerpt_re, full_anchor):
    for ex in excerpt_re:
        if ex.match(full_anchor):
            return True

    return False


def _excerpt_line(line: str) -> str:
    count = 0
    sliced_line = ""
    for c in line:
        if unicodedata.east_asian_width(c) in "FWA":
            count += 2
        else:
            count += 1

        if c == "\n":
            break

        if count > 45 and c.isspace():
            break

        if count > 55:
            break

        sliced_line += c

    if len(sliced_line) == 0:
        return ""

    return " " + sliced_line if (sliced_line[-1] == ".") else " " + sliced_line + " ..."


def gen_md_index_md(
    db: list, top_lines: [str], excerpt: [str], exclude: [str], sec_num: bool
) -> [str]:
    content = top_lines

    excerpt_re = [_gen_exc_re(ex) for ex in excerpt]

    for ex in [_gen_exc_re(ex) for ex in exclude]:
        db = [recode for recode in db if not ex.match(recode["full_anchor"])]

    last_level = 0
    for recode in db:
        section = recode["section"]
        full_anchor = recode["full_anchor"]

        if len(section) != 1:
            if last_level > len(section):  # 説が代わる
                content.append("\n")  # レベル1の前で改行

        last_level = len(section)

        sec_num_str = (
            _gen_sec_num_from_anchor(recode["anchor"]) + " " if sec_num else ""
        )
        excerpt_str = (
            _excerpt_line(recode["excerpt"])
            if _with_excerpt(excerpt_re, full_anchor)
            else ""
        )

        content.append(_gen_one_line(full_anchor, section, sec_num_str, excerpt_str))

    content += ["  \n"] * 2

    return content


class SectionDict:
    def __init__(self, db: list):
        self.__section_to_anchor = self._gen_section_to_anchor(db)

    def resolve_ref(self, md: FileContainer) -> FileContainer:
        return FileContainer(md.filename, self.resolve_ref_in_content(md.content))

    def resolve_ref_in_content(self, content: [str]) -> [str]:
        ret = [self._sub_ref_line(line) for line in content]

        return [item for item in ret if item is not None]

    def section2anchor(self, section: str) -> str:  # section may be partial
        anchors = self.__section_to_anchor[section]

        if len(anchors) == 1:
            return anchors[0]

        if not anchors:
            raise ValueError(f"{section} has no candidate")

        raise ValueError(f"{section} has many candidates\n\t" + "\n\t".join(anchors))

    def _sub_ref_line(self, line: str) -> str:
        if _MD_UMCOMPLETED_REF_RE.search(line):
            if _MD_UMCOMPLETED_REF_EXCEPT_RE.search(line):
                return line

            return _MD_UMCOMPLETED_REF_RE.sub(self._sub_ref_each, line)

        if _MD_UMCOMPLETED_REF2_RE.search(line):
            line = line.replace("](~~~)", "](---)")
            try:
                return _MD_UMCOMPLETED_REF_RE.sub(self._sub_ref_each, line)
            except:
                return None

        return line

    def _sub_ref_each(self, match_ref):
        name = match_ref.groupdict()["name"]
        anchor = self.section2anchor(name)
        index = name.rfind(_MD_SECTION_SEP)

        if index >= 0:
            name = name[index + 1 :]

        return f"[{name}]({anchor})"

    def _sec_to_str(self, section: [str]):
        return _MD_SECTION_SEP.join(section)

    def _add_db(self, section: [str], anchor: str, db: dict) -> dict:
        length = len(section)

        if len(section) == 0:
            raise ValueError(f"{anchor} has no section")

        if len(section) == 1:
            db[section[0]].append(anchor)
            db[_MD_SECTION_SEP + section[0]].append(anchor)
        else:
            for i in range(0, len(section)):
                key = self._sec_to_str(section[i:])
                db[key].append(anchor)

        return db

    def _gen_section_to_anchor(self, db: list) -> dict:
        ret = defaultdict(list)

        for recode in db:
            ret = self._add_db(recode["section"], recode["full_anchor"], ret)

        return ret
