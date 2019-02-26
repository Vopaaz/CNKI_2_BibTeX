import logging
import re
from collections import defaultdict

import jieba
from pypinyin import lazy_pinyin as pinyin

from .misc.EntryCore import Entry, NOT_FOUND_ANY
from .misc.EntryInformationCheck import (checkBibEntryHasID,
                                         checkEntryHasValidFields)
from .misc.Configure import getIDFormat


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
        for key, target in rule.items():
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
        idFormat = getIDFormat()
        if idFormat == "title":
            self.generateIDInTitleFormat(cnkiNetEntry)
        elif idFormat == "nameyear":
            self.generateIDInNameYearFormat(cnkiNetEntry)

    def generateIDInNameYearFormat(self, cnkiNetEntry):
        name = cnkiNetEntry["Author"].split(";")[0].split(",")[0].split("，")[0]
        name = name.replace(" ", "").replace(u"\u3000", "")
        year = cnkiNetEntry["Year"]
        if self.__isFullEnglish(name):
            self.ID = name + year
        else:
            self.ID = "".join([i.title() for i in pinyin(name)]) + year

    def generateIDInTitleFormat(self, cnkiNetEntry):
        title = cnkiNetEntry["Title"]
        title = re.sub(r"[0-9]", "", title)
        title = re.sub(r"[_,;]", "", title)
        if self.__isFullEnglish(title):
            titleWords = title.strip().split(" ")
            self.ID = "".join(titleWords[0:min(len(titleWords), 4)])
        else:
            jieba.setLogLevel(logging.INFO)
            title = title.replace(" ", "").replace(u"\u3000", "")
            titleWords = list(jieba.cut(title))
            stringForConvertToPinyin = "".join(
                titleWords[0:min(len(titleWords), 3)])
            self.ID = "".join(pinyin(stringForConvertToPinyin))

    def __isFullEnglish(self, string):
        return not re.search(u'[\u4e00-\u9fa5]', string)

    def generateFields(self, cnkiNetEntry):
        self.generateRequiredFieldsAndMarkRecorded(cnkiNetEntry)
        self.generateOptionalFields(cnkiNetEntry)
        self.fixEntryDifferences()

    def fixEntryDifferences(self):
        if "author" in self:
            self["author"] = self["author"].strip(";").replace(
                ";;", " and ").replace(";", " and ")
            if not self.__isFullEnglish(self["author"]):
                self["author"] = self["author"].replace(
                    ",", " and ").replace("，", " and ")
        for fieldName, fieldContent in self.items():
            self[fieldName] = fieldContent.replace(
                r"&", r"\&").replace(r"_", r"\_")

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        raise NotImplementedError

    def generateOptionalFields(self, cnkiNetEntry):
        for fieldName in cnkiNetEntry:
            if cnkiNetEntry.fieldIsNotRecorded(fieldName) and fieldName not in ["Reference Type", NOT_FOUND_ANY]:
                self.recordOneOptionalField(cnkiNetEntry, fieldName)

    def recordOneOptionalField(self, cnkiNetEntry, fieldName):
        saveFieldNames = fieldName.split("/")
        NOT_SET_LOWER_FIELD_NAME_LIST = ["ISBN", "ISSN"]
        for saveFieldName in saveFieldNames:
            saveFieldName = "".join(
                saveFieldName.strip().split(" ")).replace(",", "")
            if saveFieldName not in NOT_SET_LOWER_FIELD_NAME_LIST:
                self.fields[saveFieldName.lower()] = cnkiNetEntry[fieldName]
            else:
                self.fields[saveFieldName] = cnkiNetEntry[fieldName]
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
        string += "\n\n"
        return string


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
        if "图书印刷版ISBN" in cnkiNetEntry:
            cnkiNetEntry["ISBN"] = cnkiNetEntry.pop("图书印刷版ISBN")
        super().generateOptionalFields(cnkiNetEntry)


class Booklet(BibTeXEntry):
    rules = [{
        NOT_FOUND_ANY: NOT_FOUND_ANY
    }]  # There seems to be no entry on CNKI matches this type.


class InBook(BibTeXEntry):
    rules = [{
        NOT_FOUND_ANY: NOT_FOUND_ANY
    }]  # There seems to be no entry on CNKI matches this type.


class InCollection(BibTeXEntry):
    rules = [{
        NOT_FOUND_ANY: NOT_FOUND_ANY
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
        NOT_FOUND_ANY: NOT_FOUND_ANY
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
        NOT_FOUND_ANY: NOT_FOUND_ANY
    }]  # There seems to be no way to extract the proceeding citation info on CNKI.


class TechReport(BibTeXEntry):
    rules = [{
        NOT_FOUND_ANY: NOT_FOUND_ANY
    }]  # There seems to be no entry on CNKI matches this type.


class Unpublished(BibTeXEntry):
    rules = [{
        NOT_FOUND_ANY: NOT_FOUND_ANY
    }]  # There seems to be no entry on CNKI matches this type.


class Misc(BibTeXEntry):
    rules = [{
        NOT_FOUND_ANY: NOT_FOUND_ANY
    }]  # Misc is the entry that matches any case.

    def generateRequiredFieldsAndMarkRecorded(self, cnkiNetEntry):
        pass


class BibTeXContentStringFactory(object):
    SPECIFIED_ENTRY_TYPE_LIST = [
        Article, Book, Booklet, InBook, InCollection,
        InProceedings, Manual, MastersThesis, PhdThesis,
        Proceedings, TechReport, Unpublished
    ]

    @classmethod
    def giveBibFileContentString(cls, cnkiNetEntries):
        fullString = ""
        for cnkiEntry in cnkiNetEntries:
            foundSpecified = False
            for entryType in cls.SPECIFIED_ENTRY_TYPE_LIST:
                if entryType.cnkiNetEntryIsThisBibEntryType(cnkiEntry):
                    fullString += entryType(cnkiEntry).toBibFileString()
                    foundSpecified = True
                    break
            if not foundSpecified:
                fullString += Misc(cnkiEntry).toBibFileString()

        return fullString


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
