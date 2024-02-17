#!/usr/bin/env python3

import argparse
import requests

from plantuml import deflate_and_encode

import add_sys_path
from md_lib.file_container import FileContainer


def get_args(args=None):
    parser = argparse.ArgumentParser(description="to encode plant uml text")
    parser.add_argument("pu", nargs=1)
    parser.add_argument("-o", nargs=1)
    args = parser.parse_args(args)

    out = args.o[0] if args.o else None

    return {"pu": args.pu[0], "o": out}


def gen_str(args: dict) -> FileContainer:
    fc = FileContainer(args["pu"])

    data = "".join(fc.content)

    return f"http://www.plantuml.com/plantuml/img/{deflate_and_encode(data)}"


if __name__ == "__main__":
    args = get_args()
    pu_enc = gen_str(args)

    out_file = args["o"]
    if out_file:
        response = requests.get(pu_enc)
        with open(args["o"], "wb") as f:
            f.write(response.content)
    else:
        print(pu_enc)
