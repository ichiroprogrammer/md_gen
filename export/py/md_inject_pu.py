#!/usr/bin/env python3

import sys
import os
import argparse

import add_sys_path

from md_lib.file_container import FileContainer
from md_lib.png_ref import get_pu_content


def get_args(args=None):
    parser = argparse.ArgumentParser(description="to generate anchor, inject pu")
    parser.add_argument("md", nargs=1)
    parser.add_argument("-o", nargs=1)

    args = parser.parse_args(args)

    return {"md": args.md[0], "o": args.o[0]}


def inject_pu(args) -> FileContainer:
    fc = FileContainer(args["md"])

    new_content = []

    for line in fc.content:
        pu_content = get_pu_content(line)

        if pu_content:
            new_content.extend(pu_content)
        else:
            new_content.append(line)

    return FileContainer(args["o"], new_content)


if __name__ == "__main__":
    args = get_args()
    new_md = inject_pu(args)
    new_md.save()
