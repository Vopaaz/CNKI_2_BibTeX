from collections import defaultdict


class EntryFieldInvalidException(Exception):
    def __init__(self, className):
        self.message = "The fields of {} is invalid.".format(className)
        self.args = (self.message,)


class RequiredFieldMissingException(Exception):
    def __init__(self, fieldName):
        self.message = "The required field {} is not in the target entry.".format(
            fieldName)
        self.args = (self.message,)


class BibEntryHasNoIDException(Exception):
    def __init__(self):
        self.message = "The BibTeX entry has no ID yet."
        self.args = (self.message,)


def checkEntryHasValidFields(func):
    def inner(self, *args, **kwargs):
        if not self.fields or not isinstance(self.fields, (dict, defaultdict)):
            raise EntryFieldInvalidException(self.__class__.__name__)
        return func(self, *args, **kwargs)
    return inner


def checkBibEntryHasID(func):
    def inner(self, *args, **kwargs):
        if not self.ID:
            raise BibEntryHasNoIDException()
        return func(self, *args, **kwargs)
    return inner
