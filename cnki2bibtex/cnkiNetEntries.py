import re
from collections import defaultdict
from cnki2bibtex.misc.EntryInformationCheck import checkEntryHasValidFields
from cnki2bibtex.misc.EntryCore import Entry


class CNKINetEntry(Entry):
    '''
    One entry of CNKI .net file.
    '''

    def __init__(self):
        self.fields = defaultdict(lambda: None)
        self.recordedFieldNames = []

    def addFieldFromLine(self, stringLine):
        re_obj = re.match(r"\{(.*)\}:(.*)", stringLine)
        fieldName = re_obj.group(1).strip()
        fieldContent = re_obj.group(2).strip()
        self.fields[fieldName] = fieldContent

    def addAllFieldsFromBlock(self, stringBlock):
        for line in stringBlock.split("\n"):
            self.addFieldFromLine(line.strip())

    def __markFieldIsRecordedInBibEntry(self, key):
        if key not in self.fields:
            raise FieldNotInEntryException(key, self)
        elif key not in self.recordedFieldNames:
            self.recordedFieldNames.append(key)
        else:
            raise FieldAlreadyRecordedException(key, self)

    @checkEntryHasValidFields
    def markFieldsAreRecordedInBibEntry(self, *keys):
        for key in keys:
            self.__markFieldIsRecordedInBibEntry(key)

    @checkEntryHasValidFields
    def fieldIsNotRecorded(self, key):
        return key not in self.recordedFieldNames


class CNKINetEntryFactory(object):
    @staticmethod
    def giveAllEntries(fullTextInTheNetFile):
        entries = []
        for block in fullTextInTheNetFile.strip().split("\n\n\n"):
            tmp = CNKINetEntry()
            tmp.addAllFieldsFromBlock(block.strip())
            entries.append(tmp)
        return entries


class FieldNotInEntryException(Exception):
    def __init__(self, requiredField, entry):
        if "Title" not in entry:
            self.message = "{} is not in the entry.".format(requiredField)
        else:
            self.message = "{} is not in the entry titled {}.".format(
                requiredField, entry["Title"])

        self.args = (self.message,)


class FieldAlreadyRecordedException(Exception):
    def __init__(self, markedField, entry):
        if "Title" not in entry:
            self.message = "Field {} is already marked recorded.".format(
                markedField)
        else:
            self.message = "Field {} in entry titled {} is already marked recorded.".format(
                markedField, entry["Title"])
        self.message += " Check if there are duplicates."
        self.args = (self.message,)
