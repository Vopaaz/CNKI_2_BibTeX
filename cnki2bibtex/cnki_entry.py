import re
from collections import defaultdict

from cnki2bibtex.entry import Entry
from cnki2bibtex.misc.check import check_entry_has_valid_fields


class CNKIEntry(Entry):
    """
    One entry of CNKI .net file.
    """

    def __init__(self):
        self.fields = defaultdict(lambda: None)
        self.recorded_field_names = []

    def add_field_from_line(self, string_line):
        re_obj = re.match(r"\{(.*)\}[:：](.*)", string_line)
        field_name = re_obj.group(1).strip()
        field_content = re_obj.group(2).strip()
        self.fields[field_name] = field_content

    def add_all_fields_from_block(self, string_block):
        for line in string_block.split("\n"):
            self.add_field_from_line(line.strip())

    def __mark_field_is_recorded(self, key):
        if key not in self.fields:
            raise FieldNotInEntryException(key, self)
        elif key not in self.recorded_field_names:
            self.recorded_field_names.append(key)
        else:
            raise FieldAlreadyRecordedException(key, self)

    @check_entry_has_valid_fields
    def mark_fields_are_recorded(self, *keys):
        for key in keys:
            self.__mark_field_is_recorded(key)

    @check_entry_has_valid_fields
    def field_is_not_recorded(self, key):
        return key not in self.recorded_field_names


class CNKIEntryFactory(object):
    def give_all_entries(self, full_text_in_net_file):
        entries = []
        for block in full_text_in_net_file.strip().split(r"{Reference Type}")[1:]:
            block = r"{Reference Type}" + block.strip()
            block = self.preprocess(block)
            tmp = CNKIEntry()
            tmp.add_all_fields_from_block(block.strip())
            entries.append(tmp)
        return entries

    def preprocess(self, block):
        block = self.fix_line_break_in_content(block)
        return block

    def fix_line_break_in_content(self, block):
        block = re.sub("\n+", "\n", block)
        block = re.sub("\n([^\{])", lambda match_obj: match_obj.group(1), block)
        return block


class FieldNotInEntryException(Exception):
    def __init__(self, required_field, entry):
        if "Title" not in entry:
            self.message = "{} is not in the entry.".format(required_field)
        else:
            self.message = "{} is not in the entry titled {}.".format(required_field, entry["Title"])

        self.args = (self.message,)


class FieldAlreadyRecordedException(Exception):
    def __init__(self, marked_field, entry):
        if "Title" not in entry:
            self.message = "Field {} is already marked recorded.".format(marked_field)
        else:
            self.message = "Field {} in entry titled {} is already marked recorded.".format(
                marked_field, entry["Title"]
            )
        self.message += " Check if there are duplicates."
        self.args = (self.message,)
