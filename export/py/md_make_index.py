#!/usr/bin/env python3

import argparse
import re

import add_sys_path
from md_lib.link_ref import load_db, gen_md_index_md
from md_lib.file_container import FileContainer


def get_args(args=None):
    parser = argparse.ArgumentParser(description="to generate anchor, inject code")
    parser.add_argument("db", nargs=1)
    parser.add_argument("-o", nargs=1)
    parser.add_argument("--sec_num", action="store_true")
    parser.add_argument("--excerpt", nargs="*")
    parser.add_argument("--exclude", nargs="*")

    args = parser.parse_args(args)

    return {
        "db": args.db[0],
        "o": args.o[0],
        "sec_num": args.sec_num,
        "excerpt": args.excerpt,
        "exclude": args.exclude,
    }


def gen_fc(args: dict) -> FileContainer:
    db = load_db(args["db"])

    excerpt = args["excerpt"] if args["excerpt"] else []
    exclude = args["exclude"] if args["exclude"] else []

    index_content = gen_md_index_md(db, excerpt, exclude, args["sec_num"])

    return FileContainer(args["o"], index_content)


if __name__ == "__main__":
    args = get_args()
    fc = gen_fc(args)
    fc.save()
