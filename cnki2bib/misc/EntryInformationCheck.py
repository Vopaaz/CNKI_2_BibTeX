class EntryFieldInvalidException(Exception):
    def __init__(self, classname):
        self.message = "The fields of {classname} is invalid.".format(
            classname=classname)
        self.args = (self.message,)


def checkBibEntryInfo(func):
    def inner(self, *args, **kwargs):
        if not self.fields or not isinstance(self.fields, dict):
            raise EntryFieldInvalidException(self.__class__.__name__)
        return func(self, *args, **kwargs)
    return inner
