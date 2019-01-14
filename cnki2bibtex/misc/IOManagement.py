import os
import pyperclip

class IOManager(object):
    @staticmethod
    def getNetFileContent(path):
        if not path.endswith(".net"):
            path += ".net"
        with open(path, "r", encoding="utf8") as f:
            return f.read()

    @staticmethod
    def writeContentToBibFile(bibContentString, path):
        if not path.endswith(".bib"):
            path += ".bib"
        with open(path, "w", encoding="utf8") as f:
            f.write(bibContentString)

    @staticmethod
    def copyContentToClipboard(bibContentString):
        pyperclip.copy(bibContentString)



