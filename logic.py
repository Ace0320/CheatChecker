from difflib import SequenceMatcher
import re, os

clean = re.compile(r"//.*\n| |\n")
main = re.compile(r"^.*?int\s*main\s*\(\s*\)\s*{\s*(.+?)(?:return\s*0\s*;)?\s*}\s*$", re.S)
declare = re.compile(r"\b(?:int|float|double|char|string|bool|void)\s+(.+?)[;(]")
variable = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*[,=]?")
get_id = re.compile(r"[uU]\d{8}")


def serialize(code, only_main=True):
    if only_main:
        code = main.match(code).group(1)
    for statement in declare.findall(code):
        for var in variable.findall(statement):
            code = re.sub(r"\b{}\b".format(var), '', code)
    return clean.sub('', code)


def similarity(a, b):
    return round(SequenceMatcher(None, a, b).ratio() * 100, 1)


def get_cheaters(path="./codes/"):
    codes = {}
    matches = []
    for file_name in os.listdir(path):
        if file_name.endswith(".cpp"):
            id_ = get_id.search(file_name).group()
            code = serialize(open(os.path.join(path, file_name)).read())
            for _id, _code in codes.items():
                ratio = similarity(code, _code)
                if ratio > 60:
                    matches.append((ratio, id_, _id, file_name))
            codes[id_] = code
    return sorted(matches, reverse=True)


if __name__ == "__main__":
    for match in get_cheaters():
        print(f"{match[0]}%\t{match[1]} : {match[2]}\t{match[3]}")
