import re

from md_lib.file_container import FileContainer


class MdError:
    def __init__(self, type_num, line_num, line, last_line=""):
        self.__type_num = type_num
        self.__line_num = line_num
        self.__line = line
        self.__last_line = last_line

    def __repr__(self):
        return f"{self.__type_num}:{self.__line_num}:{self.__line}:{self.__last_line}:"

    def __eq__(self, other):
        return (
            self.__type_num == other.type_num
            and self.__line_num == other.line_num
            and self.__line == other.line
            and self.__last_line == other.last_line
        )

    @property
    def type_num(self):
        pass

    @type_num.getter
    def type_num(self):
        return self.__type_num

    @property
    def line_num(self):
        pass

    @line_num.getter
    def line_num(self):
        return self.__line_num

    @property
    def line(self):
        pass

    @line.getter
    def line(self):
        return self.__line

    @property
    def last_line(self):
        pass

    @last_line.getter
    def last_line(self):
        return self.__last_line


_BULLETS = re.compile(r"^ *\*")
_SPACE_LINE = re.compile(r"^ *$")
_QUOTE = re.compile(r"^```")


# "*"の前のラインになれないライン
def _normal_line(line):
    if _SPACE_LINE.match(line):
        return False

    if line[0] == "#":
        return False

    if _BULLETS.match(line):
        return False

    return True


def _gen_last_line(last_line, line):
    if _BULLETS.match(line):
        return line, True

    if _BULLETS.match(last_line):
        if _SPACE_LINE.match(line):  # *の終了
            return line, True
        elif _QUOTE.match(line):  # *の終了
            return line, True
        elif line[0] == " ":  # *の継続
            return (last_line.strip() + line), True
        else:
            return last_line, False

    return line, True


def find_error(md: FileContainer) -> [MdError]:
    errors = []
    line_num = 1
    last_line = "\n"
    for line in md.content:
        if line[0] == "*" and _normal_line(last_line):
            errors.append(MdError(0, line_num, line.strip(), last_line.strip()))

        last_line, error = _gen_last_line(last_line, line)

        if not error:
            errors.append(MdError(1, line_num, line.strip(), last_line.strip()))
            last_line = line

        line_num += 1

    if (not _SPACE_LINE.match(md.content[-1])) or (
        not _SPACE_LINE.match(md.content[-2])
    ):
        errors.append(MdError(2, len(md.content), "last 2 lines should be space"))

    return errors
