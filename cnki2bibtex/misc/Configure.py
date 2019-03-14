import os
import re


def setIDFormat(idFormat):
    filePath = os.path.join(os.path.expanduser('~'), r".cnki2bib.cfg")
    with open(filePath, "w", encoding="utf-8") as f:
        f.write("[settings]\nid_format = {}".format(idFormat))


def getIDFormat():
    filePath = os.path.join(os.path.expanduser('~'), r".cnki2bib.cfg")
    if os.path.exists(filePath):
        with open(filePath, "r", encoding="utf-8") as f:
            configStr = f.read()
        return re.search(r"id_format = (.*)", configStr).group(1)
    else:
        return "title"
