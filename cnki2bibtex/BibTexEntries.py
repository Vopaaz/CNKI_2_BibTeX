from cnki2bibtex.misc.EntryInformationCheck import checkEntryHasValidFields, checkBibEntryHasID
from collections import defaultdict
from cnki2bibtex.misc.EntryCore import Entry
from pypinyin import lazy_pinyin as pinyin
import jieba
import logging
import re


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
            self.ID = "".join(titleWords[0:min(len(titleWords)-1, 4)])
        else:
            jieba.setLogLevel(logging.INFO)
            titleWords = list(jieba.cut(title))
            stringForConvertToPinyin = "".join(
                titleWords[0:min(len(titleWords)-1, 3)])
            self.ID = "".join(pinyin(stringForConvertToPinyin))

    def __isFullEnglish(self, string):
        return not re.search(u'[\u4e00-\u9fa5]', string)

    def generateFields(self, cnkiNetEntry):
        self.generateRequiredFieldsAndMarkRecorded(cnkiNetEntry)
        self.generateOptionalFields(cnkiNetEntry)

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        raise NotImplementedError

    def generateOptionalFields(self, cnkiNetEntry):
        cnkiNetEntry.pop("Reference Type")
        for fieldName in cnkiNetEntry:
            if cnkiNetEntry.fieldIsNotRecorded(fieldName):
                self.recordOneOptionalField(cnkiNetEntry, fieldName)

    def recordOneOptionalField(self, cnkiNetEntry, fieldName):
        NOT_SET_LOWER_FIELD_NAME_LIST = ["ISBN"]
        if fieldName not in NOT_SET_LOWER_FIELD_NAME_LIST:
            self.fields[fieldName.lower()] = cnkiNetEntry[fieldName]
        else:
            self.fields[fieldName] = cnkiNetEntry[fieldName]
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
    pass  # Todo


class Article(BibTeXEntry):

    rules = [{
        "Reference Type": "Journal Article"
    }]

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        self["author"] = cnkiNetEntry["Author"]
        self["title"] = cnkiNetEntry["Title"]
        self["journal"] = cnkiNetEntry["Journal"]
        self["year"] = cnkiNetEntry["Year"]
        cnkiNetEntry.markFieldsAreRecordedInBibEntry(
            "Author", "Title", "Journal", "Year")


class Book(BibTeXEntry):

    rules = [{
        "Reference Type": "Book"
    }]

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        self["author"] = cnkiNetEntry["Author"]
        self["title"] = cnkiNetEntry["Title"]
        self["publisher"] = cnkiNetEntry["Publisher"]
        self["year"] = cnkiNetEntry["Date"].split("-")[0]
        cnkiNetEntry.markFieldsAreRecordedInBibEntry(
            "Author", "Title", "Publisher")

    def generateOptionalFields(self, cnkiNetEntry):
        cnkiNetEntry["month"] = cnkiNetEntry["Date"].split("-")[1]
        cnkiNetEntry["ISBN"] = cnkiNetEntry.pop("图书印刷版ISBN")
        super().generateOptionalFields(cnkiNetEntry)


class Booklet(BibTeXEntry):
    rules = [{
        "NOT_FOUND_ANY": "NOT_FOUND_ANY"
    }]  # There seems to be no entry on CNKI matches this type.


class InBook(BibTeXEntry):
    rules = [{
        "NOT_FOUND_ANY": "NOT_FOUND_ANY"
    }]  # There seems to be no entry on CNKI matches this type.


class InCollection(BibTeXEntry):
    rules = [{
        "NOT_FOUND_ANY": "NOT_FOUND_ANY"
    }]  # There seems to be no entry on CNKI matches this type.


class InProceedings(BibTeXEntry):
    rules = [{
        "Reference Type": "Conference Proceedings"
    }]

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        self["author"] = cnkiNetEntry["Author"]
        self["title"] = cnkiNetEntry["Title"]
        self["booktitle"] = cnkiNetEntry["Tertiary Title"]
        self["year"] = cnkiNetEntry["Year"]
        cnkiNetEntry.markFieldsAreRecordedInBibEntry(
            "Author", "Title", "Tertiary Title", "Year")


class Manual(BibTeXEntry):
    rules = [{
        "NOT_FOUND_ANY": "NOT_FOUND_ANY"
    }]  # There seems to be no entry on CNKI matches this type.


class MastersThesis(BibTeXEntry):
    rules = [{
        "Reference Type": "Thesis",
        "Type of Work": "硕士"
    }]

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        self["author"] = cnkiNetEntry["Author"]
        self["title"] = cnkiNetEntry["Title"]
        self["school"] = cnkiNetEntry["Publisher"]
        self["year"] = cnkiNetEntry["Year"]
        cnkiNetEntry.markFieldsAreRecordedInBibEntry(
            "Author", "Title", "Publisher", "Year"
        )

class PhdThesis(BibTeXEntry):
    rules = [{
        "Reference Type": "Thesis",
        "Type of Work": "博士"
    }]

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        self["author"] = cnkiNetEntry["Author"]
        self["title"] = cnkiNetEntry["Title"]
        self["school"] = cnkiNetEntry["Publisher"]
        self["year"] = cnkiNetEntry["Year"]
        cnkiNetEntry.markFieldsAreRecordedInBibEntry(
            "Author", "Title", "Publisher", "Year"
        )

class Proceedings(BibTeXEntry):
    rules = [{
        "NOT_FOUND_ANY": "NOT_FOUND_ANY"
    }]  # There seems to be no way to extract the proceeding citation info on CNKI.
  
class TechReport(BibTeXEntry):
    rules = [{
        "NOT_FOUND_ANY": "NOT_FOUND_ANY"
    }]  # There seems to be no entry on CNKI matches this type.

class Unpublished(BibTeXEntry):
    rules = [{
        "NOT_FOUND_ANY": "NOT_FOUND_ANY"
    }]  # There seems to be no entry on CNKI matches this type.

class Misc(BibTeXEntry):
    rules = [{
        "NOT_NECESSARY": "NOT_NECESSARY"
    }]  # Misc is the entry that matches any case.

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
