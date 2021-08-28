from collections import defaultdict


class EntryFieldInvalidException(Exception):
    def __init__(self, class_name):
        self.message = "The fields of {} is invalid.".format(class_name)
        self.args = (self.message,)


class RequiredFieldMissingException(Exception):
    def __init__(self, field_name):
        self.message = "The required field {} is not in the target entry.".format(field_name)
        self.args = (self.message,)


class BibEntryHasNoIDException(Exception):
    def __init__(self):
        self.message = "The BibTeX entry has no ID yet."
        self.args = (self.message,)


def check_entry_has_valid_fields(func):
    def inner(self, *args, **kwargs):
        if not self.fields or not isinstance(self.fields, (dict, defaultdict)):
            raise EntryFieldInvalidException(self.__class__.__name__)
        return func(self, *args, **kwargs)

    return inner


def check_bib_entry_has_id(func):
    def inner(self, *args, **kwargs):
        if not self.id:
            raise BibEntryHasNoIDException()
        return func(self, *args, **kwargs)

    return inner
