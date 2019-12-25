import glob
from cnki2bibtex.cnki2bib import getBibFileContentString
import os
import unittest
import sys
sys.path.append(".")


class IntegrationTest(unittest.TestCase):
    def test_all(self):
        self.maxDiff = 1000000
        all_bib = glob.glob("./tests/assets/*.bib")
        for bib in all_bib:
            net = os.path.splitext(bib)[0] + ".net"
            with open(bib, "r", encoding="utf-8") as b,\
                    open(net, "r", encoding="utf-8") as n:
                self.assertEqual(b.read(), getBibFileContentString(n.read()))
