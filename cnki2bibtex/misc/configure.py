import os
import re


def set_id_format(id_format):
    file_path = os.path.join(os.path.expanduser('~'), r".cnki2bib.cfg")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("[settings]\nid_format = {}".format(id_format))


def get_id_format():
    file_path = os.path.join(os.path.expanduser('~'), r".cnki2bib.cfg")
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            config_str = f.read()
        return re.search(r"id_format = (.*)", config_str).group(1)
    else:
        return "title"
