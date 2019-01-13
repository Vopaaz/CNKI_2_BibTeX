from misc.EntryInformationCheck import checkBibEntryInfo

class BibTeXEntry(object):
    def __init__(self):
        fields = dict()
        raise NotImplementedError

    def generateFields(self, cnkiNetEntry):
        raise NotImplementedError

    @checkBibEntryInfo
    def toBibFileString(self):
        raise NotImplementedError

class Article(BibTeXEntry):



if __name__ == "__main__":
    BibTeXEntry().decoratorTest(1)
