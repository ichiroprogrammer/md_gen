#!/usr/bin/env python3

import sys
import os
import argparse

import add_sys_path
from md_lib.file_container import FileContainer, find_file_in_paths
from md_lib.code_ref import inject_code, ref_srcs
from md_lib.link_ref import gen_md_anchor_all, change_png_link_to_base64
from md_lib.md_checker import MdError, find_error


def get_args(args=None):
    parser = argparse.ArgumentParser(description="to generate anchor, inject code")
    parser.add_argument("md", nargs=1)
    parser.add_argument("--mds", nargs="*")
    parser.add_argument("-D", nargs=1)
    parser.add_argument("-o", nargs=1)
    parser.add_argument("-p", type=str, default=None)  # VPATH

    args = parser.parse_args(args)

    dep = args.D[0] if args.D else None

    mds = [os.path.normpath(path) for path in args.mds] if args.mds else None

    if args.p:
        mds = [find_file_in_paths(args.p, file) for file in mds] if mds else None

    return {"md": args.md[0], "mds": mds, "D": dep, "o": args.o[0]}


def _gen_dependent_mds(d: str, md: str, mds: [str]) -> [str]:
    if not mds:
        return []

    depnds = mds[0 : mds.index(md)]

    return [f"{d}: {dep}\n" for dep in depnds]


def gen_fc(args: dict) -> FileContainer:
    from_md = FileContainer(args["md"])

    errors = find_error(from_md)

    if len(errors) != 0:
        for e in errors:
            print(e)

        sys.exit(1)

    if args["D"]:
        refs = ref_srcs(from_md)
        if refs:
            content = [f"{args['D']}: {dep}\n" for dep in refs]
        else:
            content = [f"{args['D']}: \n"]

        dep_mds = _gen_dependent_mds(args["D"], args["md"], args["mds"])

        return FileContainer(args["o"], content + dep_mds)
    else:
        mds_compiled = gen_md_anchor_all([FileContainer(md) for md in args["mds"]])
        for md in mds_compiled:
            if os.path.basename(md.filename) == os.path.basename(args["md"]):
                md = change_png_link_to_base64(md)
                content = inject_code(md)
                return FileContainer(args["o"], content)

        raise ValueError(f"bug found")


if __name__ == "__main__":
    args = get_args()
    fc = gen_fc(args)
    fc.save()
