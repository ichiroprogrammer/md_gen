import copy
import re
import os
from os import path


def related_path_in_md(md_file_path: str, file_path_in_md: str) -> str:
    dirname = path.dirname(md_file_path)

    related_path = dirname + f"/../{file_path_in_md}"

    return path.normpath(related_path)


class FileContainer:
    def __init__(self, filename, content=None):
        self.__filename = filename
        if content:
            self.__content = copy.copy(content)
        else:
            with open(filename) as f:
                self.__content = f.readlines()

    def cd(self, dir_new: str):  # change dir
        dir_org, basename = path.split(self.__filename)
        self.__filename = f"{dir_new}/{basename}"

    def mv(self, name_new: str):  # rename filename
        self.__filename = name_new

    def save(self):
        with open(self.__filename, "w") as f:
            f.writelines(self.__content)

    def __eq__(self, other):
        return self.__filename == other.filename and self.__content == other.content

    @property
    def filename(self):
        pass

    @filename.getter
    def filename(self):
        return self.__filename

    @property
    def content(self):
        pass

    @content.getter
    def content(self):
        return self.__content

#VPATH in Makefile
#VPATH空のパスの補完

def find_file_in_paths(vpath, file):
    paths = re.split(r'[ :]', vpath) if vpath else None

    if not paths:
        return None
        
    for path in paths:
        file_path = os.path.join(path, file)
        if os.path.exists(file_path):
            return file_path
    return None

