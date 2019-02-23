import re
from collections import defaultdict

from .misc.EntryCore import Entry
from .misc.EntryInformationCheck import checkEntryHasValidFields


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
    def giveAllEntries(self, fullTextInTheNetFile):
        entries = []
        for block in fullTextInTheNetFile.strip().split(r"{Reference Type}")[1:]:
            block = r"{Reference Type}" + block.strip()
            block = self.preprocessingBlock(block)
            tmp = CNKINetEntry()
            tmp.addAllFieldsFromBlock(block.strip())
            entries.append(tmp)
        return entries

    def preprocessingBlock(self, block):
        block = self.fixLineBreakInContent(block)
        return block

    def fixLineBreakInContent(self, block):
        block = re.sub("\n+", "\n", block)
        block = re.sub("\n([^\{])", lambda matchObj: matchObj.group(1), block)
        return block


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
