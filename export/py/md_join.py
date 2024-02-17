#!/usr/bin/env python3

import argparse

import add_sys_path
from md_lib.file_container import FileContainer
from md_lib.link_ref import del_filename_in_link


def get_args(args=None):
    parser = argparse.ArgumentParser(description="from markdown to html")
    parser.add_argument("mds", nargs="+")
    parser.add_argument("-o", nargs=1)
    args = parser.parse_args(args)

    return {"mds": args.mds, "o": args.o[0]}


def gen_fc(args: dict) -> FileContainer:
    all_content = []

    for fc in [FileContainer(md) for md in args["mds"]]:
        all_content += fc.content

    return FileContainer(args["o"], del_filename_in_link(all_content))


if __name__ == "__main__":
    args = get_args()
    fc = gen_fc(args)
    fc.save()
