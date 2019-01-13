from cnki2bib.misc.EntryInformationCheck import checkEntryHasValidFields, RequiredFieldMissingException
from collections import defaultdict
import warnings

class Entry(object):
    def __init__(self):
        self.fields = defaultdict(lambda: None)

    @checkEntryHasValidFields
    def __getitem__(self, key):
        field = self.fields[key]
        if not field:
            warnings.warn("The {} field in the entry is Empty. Returned as string 'Null'.".format(key))
            field = "Null"
        return field

    @checkEntryHasValidFields
    def __iter__(self):
        return self.fields.__iter__()

    def items(self):
        return self.fields.items()

    @checkEntryHasValidFields
    def __contains__(self, key):
        return key in self.fields

    def __setitem__(self, key, value):
        self.fields[key] = value
