#!/usr/bin/env python3

import argparse

import add_sys_path
from md_lib.file_container import FileContainer
from md_lib.link_ref import gen_md_section_db, store_db


def get_args(args=None):
    parser = argparse.ArgumentParser(description="to generate anchor, inject code")
    parser.add_argument("db", nargs=1)
    parser.add_argument("--mds", nargs="+")

    args = parser.parse_args(args)

    return {"db": args.db[0], "mds": args.mds}


def gen_db(args: dict) -> FileContainer:
    return gen_md_section_db([FileContainer(fc) for fc in args["mds"]])


if __name__ == "__main__":
    args = get_args()
    content = gen_db(args)

    store_db(args["db"], content)
