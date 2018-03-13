from difflib import SequenceMatcher
from collections import OrderedDict
import re, os

clean = re.compile(r"//.*\n| |\n")
main = re.compile(r"^.*?int\s*main\s*\(\s*\)\s*{\s*(.+?)(?:return\s*0\s*;)?\s*}\s*$", re.S)
declare = re.compile(r"\b(?:int|float|double|char|string|bool|void)\s+(.+?)[;(]")
variable = re.compile(r"([a-zA-Z_][a-zA-Z0-9_]*)\s*[,=]?")
get_id = re.compile(r"[uU]\d{8}")


def serialize(code, only_main=True):
    if only_main:
        try: code = main.match(code).group(1)
        except AttributeError: return False
    for statement in declare.findall(code):
        for var in variable.findall(statement):
            code = re.sub(r"\b{}\b".format(var), '', code)
    return clean.sub('', code)


def similarity(a, b):
    return round(SequenceMatcher(None, a, b).ratio() * 100, 1)


def get_cheaters(path="./codes/"):
    cheaters = {}
    matches = []
    for file_name in os.listdir(path):
        if file_name.endswith(".cpp"):
            id_ = get_id.search(file_name).group()
            code = serialize(open(os.path.join(path, file_name)).read())
            if not code: continue
            for _id, file in cheaters.items():
                ratio = similarity(code, file["code"])
                if ratio > 40:
                    matches.append((f"{ratio}% {id_}:{_id}", [file_name, file["name"]]))
            cheaters[id_] = {"code": code, "name": file_name}
    return OrderedDict(sorted(matches, key=lambda m: float(m[0].split("%")[0]), reverse=True))


if __name__ == "__main__":
    for match in get_cheaters().keys():
        print(match)
