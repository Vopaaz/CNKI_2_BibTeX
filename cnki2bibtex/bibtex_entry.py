import logging
import re
from collections import defaultdict

import jieba
from pypinyin import lazy_pinyin as pinyin

from cnki2bibtex.entry import Entry, NOT_FOUND
from cnki2bibtex.misc.check import check_entry_has_valid_fields, check_bib_entry_has_id
from cnki2bibtex.misc.configure import get_id_format


class BibTeXEntry(Entry):

    rules = []

    @classmethod
    def cnki_entry_is_this_bib_entry_type(cls, cnki_entry):
        if not cls.rules or not isinstance(cls.rules, list):
            raise RulesNotValidException(cls.rules)
        for rule in cls.rules:
            if cls.__cnki_entry_match_this_rule(cnki_entry, rule):
                return True
        return False

    @staticmethod
    def __cnki_entry_match_this_rule(cnki_entry, rule):
        for key, target in rule.items():
            if cnki_entry[key] != target:
                return False
        return True

    def __init__(self, cnki_entry=None):
        self.fields = defaultdict(lambda: None)
        self.id = None
        if cnki_entry:
            self.generate_fields(cnki_entry)
            self.generate_id(cnki_entry)

    def generate_id(self, cnki_entry):
        id_format = get_id_format()
        if id_format == "title":
            self.generate_id_in_title_format(cnki_entry)
        elif id_format == "nameyear":
            self.generate_id_in_name_year_format(cnki_entry)

    def generate_id_in_name_year_format(self, cnki_entry):
        name = cnki_entry["Author"].split(";")[0].split(",")[0].split("，")[0]
        name = name.replace(" ", "").replace(u"\u3000", "")
        year = cnki_entry["Year"]
        if self.__is_full_english(name):
            self.id = name + year
        else:
            self.id = "".join([i.title() for i in pinyin(name)]) + year

    def generate_id_in_title_format(self, cnki_entry):
        title = cnki_entry["Title"]
        title = re.sub(r"[0-9]", "", title)
        title = re.sub(r"[_,;]", "", title)
        if self.__is_full_english(title):
            title_words = title.strip().split(" ")
            self.id = "".join(title_words[0 : min(len(title_words), 4)])
        else:
            jieba.setLogLevel(logging.INFO)
            title = title.replace(" ", "").replace(u"\u3000", "")
            title_words = list(jieba.cut(title))
            string_to_convert = "".join(title_words[0 : min(len(title_words), 3)])
            self.id = "".join(pinyin(string_to_convert))

    def __is_full_english(self, string):
        return not re.search(u"[\u4e00-\u9fa5]", string)

    def generate_fields(self, cnki_entry):
        self.generate_required_fields_and_mark_recorded(cnki_entry)
        self.generate_optional_fields(cnki_entry)
        self.fix_entry_differences()

    def fix_entry_differences(self):
        if "author" in self:
            self["author"] = self["author"].strip(";").replace(";;", " and ").replace(";", " and ")
            if not self.__is_full_english(self["author"]):
                self["author"] = self["author"].replace(",", " and ").replace("，", " and ")
        for field_name, field_content in self.items():
            self[field_name] = field_content.replace(r"&", r"\&").replace(r"_", r"\_")

    def generate_required_fields_and_mark_recorded(self, cnki_entry):
        raise NotImplementedError

    def generate_optional_fields(self, cnki_entry):
        for field_name in cnki_entry:
            if cnki_entry.field_is_not_recorded(field_name) and field_name not in ["Reference Type", NOT_FOUND]:
                self.record_one_optional_field(cnki_entry, field_name)

    def record_one_optional_field(self, cnki_entry, field_name):
        save_field_names = field_name.split("/")
        NOT_SET_LOWER_FIELD_NAME_LIST = ["ISBN", "ISSN"]
        for save_field_name in save_field_names:
            save_field_name = "".join(save_field_name.strip().split(" ")).replace(",", "")
            if save_field_name not in NOT_SET_LOWER_FIELD_NAME_LIST:
                self.fields[save_field_name.lower()] = cnki_entry[field_name]
            else:
                self.fields[save_field_name] = cnki_entry[field_name]
        cnki_entry.mark_fields_are_recorded(field_name)

    @check_entry_has_valid_fields
    @check_bib_entry_has_id
    def to_bib_file_string(self):
        string = ""
        string += r"@"
        string += self.__class__.__name__
        string += r"{"
        string += self.id
        string += ",\n"
        for key, value in self.items():
            string += "\t{key} = {{{value}}},\n".format(key=key, value=value)
        string += r"}"
        string += "\n\n"
        return string


class Article(BibTeXEntry):

    rules = [{"Reference Type": "Journal Article"}]

    def generate_required_fields_and_mark_recorded(self, cnki_entry):
        self["author"] = cnki_entry["Author"]
        self["title"] = cnki_entry["Title"]
        self["journal"] = cnki_entry["Journal"]
        self["year"] = cnki_entry["Year"]
        cnki_entry.mark_fields_are_recorded("Author", "Title", "Journal", "Year")


class Book(BibTeXEntry):

    rules = [{"Reference Type": "Book"}]

    def generate_required_fields_and_mark_recorded(self, cnki_entry):
        self["author"] = cnki_entry["Author"]
        self["title"] = cnki_entry["Title"]
        self["publisher"] = cnki_entry["Publisher"]
        self["year"] = cnki_entry["Date"].split("-")[0]
        cnki_entry.mark_fields_are_recorded("Author", "Title", "Publisher")

    def generate_optional_fields(self, cnki_entry):
        cnki_entry["month"] = cnki_entry["Date"].split("-")[1]
        if "图书印刷版ISBN" in cnki_entry:
            cnki_entry["ISBN"] = cnki_entry.pop("图书印刷版ISBN")
        super().generate_optional_fields(cnki_entry)


class Booklet(BibTeXEntry):
    rules = [{NOT_FOUND: NOT_FOUND}]  # There seems to be no entry on CNKI matches this type.


class InBook(BibTeXEntry):
    rules = [{NOT_FOUND: NOT_FOUND}]  # There seems to be no entry on CNKI matches this type.


class InCollection(BibTeXEntry):
    rules = [{NOT_FOUND: NOT_FOUND}]  # There seems to be no entry on CNKI matches this type.


class InProceedings(BibTeXEntry):
    rules = [{"Reference Type": "Conference Proceedings"}]

    def generate_required_fields_and_mark_recorded(self, cnki_entry):
        self["author"] = cnki_entry["Author"]
        self["title"] = cnki_entry["Title"]
        self["booktitle"] = cnki_entry["Tertiary Title"]
        self["year"] = cnki_entry["Year"]
        cnki_entry.mark_fields_are_recorded("Author", "Title", "Tertiary Title", "Year")


class Manual(BibTeXEntry):
    rules = [{NOT_FOUND: NOT_FOUND}]  # There seems to be no entry on CNKI matches this type.


class MastersThesis(BibTeXEntry):
    rules = [{"Reference Type": "Thesis", "Type of Work": "硕士"}]

    def generate_required_fields_and_mark_recorded(self, cnki_entry):
        self["author"] = cnki_entry["Author"]
        self["title"] = cnki_entry["Title"]
        self["school"] = cnki_entry["Publisher"]
        self["year"] = cnki_entry["Year"]
        cnki_entry.mark_fields_are_recorded("Author", "Title", "Publisher", "Year")


class PhdThesis(BibTeXEntry):
    rules = [{"Reference Type": "Thesis", "Type of Work": "博士"}]

    def generate_required_fields_and_mark_recorded(self, cnki_entry):
        self["author"] = cnki_entry["Author"]
        self["title"] = cnki_entry["Title"]
        self["school"] = cnki_entry["Publisher"]
        self["year"] = cnki_entry["Year"]
        cnki_entry.mark_fields_are_recorded("Author", "Title", "Publisher", "Year")


class Proceedings(BibTeXEntry):
    rules = [{NOT_FOUND: NOT_FOUND}]  # There seems to be no way to extract the proceeding citation info on CNKI.


class TechReport(BibTeXEntry):
    rules = [{NOT_FOUND: NOT_FOUND}]  # There seems to be no entry on CNKI matches this type.


class Unpublished(BibTeXEntry):
    rules = [{NOT_FOUND: NOT_FOUND}]  # There seems to be no entry on CNKI matches this type.


class Misc(BibTeXEntry):
    rules = [{NOT_FOUND: NOT_FOUND}]  # Misc is the entry that matches any case.

    def generate_required_fields_and_mark_recorded(self, cnki_entry):
        pass


class BibTeXContentStringFactory(object):
    SPECIFIED_ENTRY_TYPE_LIST = [
        Article,
        Book,
        Booklet,
        InBook,
        InCollection,
        InProceedings,
        Manual,
        MastersThesis,
        PhdThesis,
        Proceedings,
        TechReport,
        Unpublished,
    ]

    @classmethod
    def give_bib_file_content_string(cls, cnki_entries):
        full_string = ""
        for cnki_entry in cnki_entries:
            found = False

            for entry_type in cls.SPECIFIED_ENTRY_TYPE_LIST:
                if entry_type.cnki_entry_is_this_bib_entry_type(cnki_entry):
                    full_string += entry_type(cnki_entry).to_bib_file_string()
                    found = True
                    break

            if not found:
                full_string += Misc(cnki_entry).to_bib_file_string()

        return full_string


class RulesNotValidException(Exception):
    def __init__(self, rules):
        self.message = str(rules) + " is not valid. It should be a list whose elements are dictionaries."
        self.args = (self.message,)


class OneRuleIsNotValidException(Exception):
    def __init__(self, rule):
        self.message = str(rule) + " is not valid. It should be a dictionary whose values are simply String."
        self.args = (self.message,)

