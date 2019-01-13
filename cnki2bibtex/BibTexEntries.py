from cnki2bibtex.misc.EntryInformationCheck import checkEntryHasValidFields, checkBibEntryHasID
from collections import defaultdict
from cnki2bibtex.misc.EntryCore import Entry
from pypinyin import lazy_pinyin as pinyin
import jieba


class BibTeXEntry(Entry):

    rules = []

    @classmethod
    def cnkiNetEntryIsThisBibEntryType(cls, cnkiNetEntry):
        if not cls.rules or not isinstance(cls.rules, list):
            raise RulesNotValidException(cls.rules)
        for rule in cls.rules:
            if cls.__cnkiNetEntryMatchThisRule(cnkiNetEntry, rule):
                return True
        return False

    @staticmethod
    def __cnkiNetEntryMatchThisRule(cnkiNetEntry, rule):
        for key, target in rule:
            if cnkiNetEntry[key] != target:
                return False
        return True

    def __init__(self, cnkiNetEntry=None):
        self.fields = defaultdict(lambda: None)
        self.ID = None
        if cnkiNetEntry:
            self.generateFields(cnkiNetEntry)
            self.generateID(cnkiNetEntry)

    def generateID(self, cnkiNetEntry):
        title = cnkiNetEntry["Title"]
        if self.__isFullEnglish(title):
            titleWords = title.strip().split(" ")
            self.ID = "".join(titleWords[0:min(len(titleWords)-1, 3)])
        else:
            titleWords = list(jieba.cut(title))
            stringForConvertToPinyin = "".join(
                titleWords[0:min(len(titleWords)-1, 3)])
            self.ID = "".join(pinyin(stringForConvertToPinyin))

    def __isFullEnglish(self, string):
        string.replace(" ", "")
        return string.isalpha() or string.isalnum()

    def generateFields(self, cnkiNetEntry):
        self.generateRequiredFieldsAndMarkRecorded(cnkiNetEntry)
        self.generateOptionalFields(cnkiNetEntry)

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        raise NotImplementedError

    def generateOptionalFields(self, cnkiNetEntry):
        for fieldName, fieldContent in cnkiNetEntry.items():
            if cnkiNetEntry.fieldIsNotRecorded(fieldName):
                self.fields[fieldName] = fieldContent
                cnkiNetEntry.markFieldsAreRecordedInBibEntry(fieldName)

    @checkEntryHasValidFields
    @checkBibEntryHasID
    def toBibFileString(self):
        string = ""
        string += r"@"
        string += self.__class__.__name__
        string += r"{"
        string += self.ID
        string += ",\n"
        for key, value in self.items():
            string += "\t{key} = {{{value}}},\n".format(key=key, value=value)
        string += r"}"
        string += "\n"
        return string

class BibTeXEntriesFactory(object):
    pass


class Article(BibTeXEntry):

    rules = [{
        "Reference Type": "Journal Article"
    }]

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        self["author"] = cnkiNetEntry["Author"]
        self["title"] = cnkiNetEntry["Title"]
        self["journal"] = cnkiNetEntry["Journal"]
        self["year"] = cnkiNetEntry["Year"]
        cnkiNetEntry.markFieldsAreRecordedInBibEntry("Author","Title","Journal","Year")


class RulesNotValidException(Exception):
    def __init__(self, rules):
        self.message = str(
            rules) + " is not valid. It should be a list whose elements are dictionaries."
        self.args = (self.message, )


class OneRuleIsNotValidException(Exception):
    def __init__(self, rule):
        self.message = str(
            rule) + " is not valid. It should be a dictionary whose values are simply String."
        self.args = (self.message, )
