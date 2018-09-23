import parse
import sys


def is_valid(line):
    if line is not "\n" and line.split("//")[0] and "(" not in line.split("//")[0]:
        return True


if __name__ == '__main__':
    parser = parse.Parser()
    pos = 0
    with open(sys.argv[1]) as f:
        for line in f:
            line = line.replace(" ", "").replace("\n", "")
            if not line: continue
            if "(" in line.split("//")[0]:
                parser.set_label(line.split("//")[0], pos)
            elif "@" in line.split("//")[0]:
                parser.set_symbol(line.split("//")[0])
            if is_valid(line):
                pos += 1
    with open(sys.argv[1]) as f:
        with open(sys.argv[1].split(".")[0]+".hack", "w") as result:
            for line in f:
                line = line.replace(" ", "").replace("\n", "")
                if not line: continue
                if "//" in line:
                    if line.split("//")[0]:
                        result.write(parser.parse(line.split("//")[0]) + "\n")
                elif line is not "\n" and "(" not in line:
                    result.write(parser.parse(line)+"\n")

