#!/usr/bin/env python3

import argparse
import glob

import add_sys_path
from md_lib.file_container import FileContainer
from md_lib.link_ref import gen_md_section_db, store_db
from md_lib.code_ref import ref_srcs_by_dict, gen_sample_file_section


def get_args(args=None):
    parser = argparse.ArgumentParser(description="to generate sample code section")
    parser.add_argument("mds", nargs="+")
    parser.add_argument("--python")
    parser.add_argument("-o", nargs=1)

    args = parser.parse_args(args)

    return {
        "mds": args.mds,
        "python": args.python,
        "o": args.o[0],
    }


def gen_fc(args: dict) -> FileContainer:
    mds = [FileContainer(fc) for fc in args["mds"]]

    refs = ref_srcs_by_dict(mds)
    content = gen_sample_file_section(refs)

    return FileContainer(args["o"], content)


if __name__ == "__main__":
    args = get_args()
    fc = gen_fc(args)
    fc.save()
