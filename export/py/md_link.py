#!/usr/bin/env python3

import argparse

import add_sys_path
from md_lib.file_container import FileContainer
from md_lib.link_ref import SectionDict, load_db, add_sec_num, inject_index


def get_args(args=None):
    parser = argparse.ArgumentParser(description="to resolve link in markdown")
    parser.add_argument("md", nargs=1)
    parser.add_argument("-o", nargs=1)
    parser.add_argument("--db", nargs=1)
    parser.add_argument("--sec_num", action="store_true")

    args = parser.parse_args(args)

    return {"md": args.md[0], "o": args.o[0], "db": args.db[0], "sec_num": args.sec_num}


def gen_fc(args: dict) -> FileContainer:
    md = FileContainer(args["md"])
    sd = SectionDict(load_db(args["db"]))

    content = sd.resolve_ref_in_content(md.content)

    new_content = inject_index(md, content)

    if args["sec_num"]:
        new_content = add_sec_num(new_content)

    return FileContainer(args["o"], new_content)


if __name__ == "__main__":
    args = get_args()
    fc = gen_fc(args)
    fc.save()
