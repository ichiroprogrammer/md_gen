#!/usr/bin/env python3

import argparse
import re

import add_sys_path
from md_lib.file_container import FileContainer
from md_lib.link_ref import SectionDict, load_db, add_sec_num, inject_index


def get_args(args=None):
    parser = argparse.ArgumentParser(description="to resolve link in markdown")
    parser.add_argument("md", nargs=1)
    parser.add_argument("-o", nargs=1)
    parser.add_argument("--db", nargs=1)
    parser.add_argument("--ig", nargs=1)
    parser.add_argument("--sec_num", action="store_true")

    args = parser.parse_args(args)

    if not args.ig:
        ig = None
    else:
        ig = args.ig[0]

    return {
        "md": args.md[0],
        "o": args.o[0],
        "db": args.db[0],
        "ig": ig,
        "sec_num": args.sec_num,
    }


def _next_ss_anchor(db, filename) -> str:
    pattern = re.compile(r"^SS_[0-9]+$")

    ss_tops = [
        d for d in db if isinstance(d.get("anchor"), str) and pattern.match(d["anchor"])
    ]

    index = next(
        (i for i, d in enumerate(ss_tops) if d.get("filename") == filename), None
    )

    if not index:
        return None

    target = ss_tops[index + 1] if (index + 1) < len(ss_tops) else None

    return target["full_anchor"] if target else None


def gen_fc(args: dict) -> FileContainer:
    md = FileContainer(args["md"])
    md_filename = args["md"].split("/")[-1]
    db = load_db(args["db"])
    sd = SectionDict(db, args["ig"])

    content = sd.resolve_ref_in_content(md.content)

    next_ss_anchor = _next_ss_anchor(db, md_filename)

    new_content = inject_index(md, content, args["sec_num"], next_ss_anchor)

    if args["sec_num"]:
        new_content = add_sec_num(new_content)

    return FileContainer(args["o"], new_content)


if __name__ == "__main__":
    args = get_args()
    fc = gen_fc(args)
    fc.save()
