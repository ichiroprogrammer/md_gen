#!/usr/bin/env python3

import sys
from PIL import Image


def is_too_wide(png: str):
    with Image.open(png) as im:
        return im.width > 750


if __name__ == "__main__":
    png = sys.argv[1]
    if is_too_wide(png):
        print(f"{png} is too wide !!!\n")
        sys.exit(1)
