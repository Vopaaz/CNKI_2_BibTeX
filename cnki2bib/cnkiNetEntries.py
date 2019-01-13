import re
from collections import defaultdict


class CNKINetEntry(object):
    '''
    One entry of CNKI .net file.
    '''

    def __init__(self):
        self.fields = defaultdict(lambda: None)

    def addFieldFromLine(self, stringLine):
        re_obj = re.match(r"\{(.*)\}:(.*)", stringLine)
        fieldName = re_obj.group(1).strip()
        fieldContent = re_obj.group(2).strip()
        self.fields[fieldName] = fieldContent

    def addAllFieldsFromBlock(self, stringBlock):
        for line in stringBlock.split("\n"):
            self.addFieldFromLine(line.strip())


class CNKINetEntryFactory(object):
    @classmethod
    def giveAllEntries(self, fullTextInTheNetFile):
        entries = []
        for block in fullTextInTheNetFile.strip().split("\n\n\n"):
            tmp = CNKINetEntry()
            tmp.addAllFieldsFromBlock(block.strip())
            entries.append(tmp)
        return entries
