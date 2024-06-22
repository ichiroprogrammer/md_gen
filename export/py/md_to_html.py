#!/usr/bin/env python3

import argparse
import subprocess

import add_sys_path
from md_lib.file_container import FileContainer
from md_lib.to_html import adjust_html


def get_args(args=None):
    parser = argparse.ArgumentParser(description="from markdown to html")
    parser.add_argument("md", nargs=1)
    parser.add_argument("-o", nargs=1)
    parser.add_argument("--author", nargs=1)
    parser.add_argument("--title", nargs=1)

    args = parser.parse_args(args)

    author = args.author[0] if args.author else "anonimous"
    return {
        "md": args.md[0],
        "title": args.title[0],
        "author": author,
        "o": args.o[0],
    }


def gen_fc(args: dict) -> FileContainer:
    pandoc_version = subprocess.check_output(["pandoc", "--version"]).decode("utf-8")

    if "3.2" not in pandoc_version:
        print("Warning: Pandoc version may not be compatible with this code.")

    cmd = [
        "pandoc",
        "-V",
        f'author=autor:{args["author"]}',
        "--highlight-style=zenburn",
        "--metadata",
        f'title={args["title"]}',
        "--standalone",
        args["md"],
    ]

    res = subprocess.check_output(cmd, encoding="utf-8")
    content = res.splitlines(True)

    return adjust_html(FileContainer(args["o"], content))


if __name__ == "__main__":
    args = get_args()
    fc = gen_fc(args)
    fc.save()
