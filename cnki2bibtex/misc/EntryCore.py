import logging
import warnings
from collections import defaultdict

from .EntryInformationCheck import (RequiredFieldMissingException,
                                    checkEntryHasValidFields)

NOT_FOUND_ANY = ""


class Entry(object):
    def __init__(self):
        self.fields = defaultdict(lambda: None)

    @checkEntryHasValidFields
    def __getitem__(self, key):
        field = self.fields[key]
        if key not in [NOT_FOUND_ANY] and not field:
            field = "Null"
            logger = logging.getLogger(__name__)
            if "Title" not in self.fields:
                logger.warning(
                    "The {} field in the entry is Empty. Returned as string 'Null'.".format(key))
            else:
                logger.warning("The {} field in the entry titled {} is Empty. Returned as string 'Null'.".format(
                    key, self.fields["Title"]))
        return field

    @checkEntryHasValidFields
    def __iter__(self):
        return self.fields.__iter__()

    @checkEntryHasValidFields
    def items(self):
        return self.fields.items()

    @checkEntryHasValidFields
    def __contains__(self, key):
        return key in self.fields

    def __setitem__(self, key, value):
        self.fields[key] = value

    def pop(self, key):
        return self.fields.pop(key)
